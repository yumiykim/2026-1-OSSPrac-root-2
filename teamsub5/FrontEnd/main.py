from flask import Flask, render_template, redirect, url_for, session, abort, request
from dotenv import load_dotenv
from datetime import datetime
from io import BytesIO
import os
import json
import uuid

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

DATA_FILE = os.path.join(app.root_path, "data", "members.json")
BOARD_RUNTIME_DIR = os.path.join(app.root_path, "instance", "board")
POSTS_SEED_FILE = os.path.join(app.root_path, "data", "posts.json")
COMMENTS_SEED_FILE = os.path.join(app.root_path, "data", "comments.json")
POSTS_RUNTIME_FILE = os.path.join(BOARD_RUNTIME_DIR, "posts.json")
COMMENTS_RUNTIME_FILE = os.path.join(BOARD_RUNTIME_DIR, "comments.json")

UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
ALLOWED_PORTFOLIO_EXTENSIONS = {
    "pdf", "doc", "docx", "ppt", "pptx", "xls", "xlsx", "zip",
    "png", "jpg", "jpeg", "gif", "webp"
}
PREDEFINED_LANGUAGES = {"Python", "Java", "C/C++", "HTML/CSS", "SQL"}
GEMINI_IMAGE_MODEL = os.getenv("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def load_root_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_root_team():
    data = load_root_data()
    return data.get("team", {})


def load_root_members():
    data = load_root_data()
    return data.get("members", [])


def get_root_member_by_id(member_id):
    members = load_root_members()

    for member in members:
        if int(member.get("id")) == member_id:
            return member

    return None


def init_generated_team():
    if "generated_team" not in session:
        session["generated_team"] = {
            "team_name": "",
            "team_intro": "",
            "team_image": "images/default-team.png",
            "members": [],
            "next_member_id": 1000
        }


def get_generated_team():
    init_generated_team()
    return session["generated_team"]


def save_generated_team(team):
    session["generated_team"] = team
    session.modified = True


def get_generated_member_by_id(member_id):
    team = get_generated_team()

    for member in team.get("members", []):
        if int(member.get("id")) == member_id:
            return member

    return None

def allowed_file(filename, allowed_extensions=ALLOWED_EXTENSIONS):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def save_uploaded_file(file, default_path):
    if file is None or file.filename == "":
        return default_path

    if not allowed_file(file.filename):
        return default_path

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    ext = file.filename.rsplit(".", 1)[1].lower()
    new_filename = f"{uuid.uuid4().hex}.{ext}"

    save_path = os.path.join(app.config["UPLOAD_FOLDER"], new_filename)
    file.save(save_path)

    return f"uploads/{new_filename}"


def save_uploaded_asset(file, default_path="", default_name="", subfolder="", allowed_extensions=None):
    if file is None or file.filename == "":
        return default_path, default_name

    allowed_extensions = allowed_extensions or ALLOWED_EXTENSIONS
    if not allowed_file(file.filename, allowed_extensions):
        return default_path, default_name

    upload_folder = os.path.join(app.config["UPLOAD_FOLDER"], subfolder)
    os.makedirs(upload_folder, exist_ok=True)

    ext = file.filename.rsplit(".", 1)[1].lower()
    new_filename = f"{uuid.uuid4().hex}.{ext}"

    save_path = os.path.join(upload_folder, new_filename)
    file.save(save_path)

    upload_path = f"uploads/{new_filename}" if not subfolder else f"uploads/{subfolder}/{new_filename}"
    return upload_path, file.filename


def build_image_prompt(image_type, user_prompt, team=None, member=None):
    base_style = (
        "Create a polished, friendly image for a personal introduction website. "
        "No readable text, no letters, no numbers, no captions, no watermark-like logo. "
        "Clean composition, modern but warm, cute and approachable."
    )

    if image_type == "team":
        return (
            f"{base_style} Make a representative square team image in an iPhone Memoji-inspired "
            f"3D cartoon style — not photorealistic, cute and polished, soft lighting, "
            f"simple clean background. "
            f"This is a team identity image, not individual portraits: "
            f"use a logo, icon, mascot, or group concept that represents the team as a whole. "
            f"If the image includes any human characters, give them East Asian skin tone and dark hair, "
        f"but with large expressive rounded eyes, well-defined nose, and full lips "
        f"in a Memoji / Pixar 3D cartoon style. "
            f"1:1 aspect ratio. "
            f"Team name: {team.get('team_name', '') if team else ''}. "
            f"Team intro: {team.get('team_intro', '') if team else ''}. "
            f"The user request may be written in Korean; interpret it naturally. "
            f"User request: {user_prompt}"
        )

    return (
        f"{base_style} Make a square cute animated avatar portrait in an iPhone "
        f"Memoji-inspired 3D cartoon style. Not photorealistic, not an ID photo, "
        f"adult person only, rounded face, East Asian skin tone and dark hair, "
        f"large expressive rounded eyes, well-defined nose, and full lips "
        f"in a Memoji / Pixar 3D cartoon style, soft lighting, simple background. "
        f"Do not include name, major, role, programming languages, or any other text information "
        f"inside the image. "
        f"The user request may be written in Korean; interpret it naturally. "
        f"User request: {user_prompt}"
    )


def generate_gemini_image(prompt, subfolder="ai", aspect_ratio="1:1"):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    try:
        from google import genai
        from google.genai import errors
        from google.genai import types
        from PIL import Image
    except ImportError:
        return None

    client = genai.Client(api_key=api_key)
    try:
        response = client.models.generate_content(
            model=GEMINI_IMAGE_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(aspect_ratio=aspect_ratio)
            )
        )
    except errors.APIError:
        return None

    if not response.candidates:
        return None

    content = response.candidates[0].content
    if not content or not getattr(content, "parts", None):
        return None

    for part in content.parts:
        if not getattr(part, "inline_data", None):
            continue

        image_bytes = part.inline_data.data
        image = Image.open(BytesIO(image_bytes))

        upload_folder = os.path.join(app.config["UPLOAD_FOLDER"], subfolder)
        os.makedirs(upload_folder, exist_ok=True)

        filename = f"{uuid.uuid4().hex}.png"
        save_path = os.path.join(upload_folder, filename)
        image.save(save_path, format="PNG")

        return f"uploads/{subfolder}/{filename}"

    return None


@app.route("/")
def index():
    team = load_root_team()
    members = load_root_members()

    return render_template(
        "index.html",
        team=team,
        members=members
    )

@app.route("/team-page")
def team_page_entry():
    team = get_generated_team()
    has_generated_team = bool(
        team.get("team_name") or
        team.get("team_intro") or
        team.get("members")
    )

    if has_generated_team:
        return redirect(url_for("result"))

    return redirect(url_for("input_page"))

@app.route("/input")
def input_page():
    team = get_generated_team()
    member_id = request.args.get("member_id", type=int)
    edit_team = request.args.get("edit_team") == "1"

    members = team.get("members", [])
    member = None
    member_index = None
    member_custom_language = ""
    if member_id:
        for idx, generated_member in enumerate(members):
            if int(generated_member.get("id")) == member_id:
                member = generated_member
                member_index = idx
                break

        if member is None:
            abort(404)

        custom_languages = [
            language
            for language in member.get("languages", [])
            if language not in PREDEFINED_LANGUAGES
        ]
        member_custom_language = ", ".join(custom_languages)

    return render_template(
        "input.html",
        team=team,
        member=member,
        member_index=member_index,
        member_position=member_index + 1 if member_index is not None else None,
        member_custom_language=member_custom_language,
        member_count=len(members),
        is_edit_flow=request.args.get("flow") == "edit",
        edit_team=edit_team
    )
    
@app.route("/reset")
def reset_team():
    session.pop("generated_team", None)
    return redirect(url_for('input_page'))

@app.route("/member/update", methods=["POST"])
def update_member():
    team = get_generated_team()

    team["team_name"] = request.form.get("team_name", team.get("team_name", "")).strip()
    team["team_intro"] = request.form.get("team_intro", team.get("team_intro", "")).strip()

    team_image = request.files.get("team_image")
    team_prompt = request.form.get("team_prompt", "").strip()
    old_team_image = team.get("team_image", "images/default-team.png")

    if team_image and team_image.filename:
        team["team_image"] = save_uploaded_file(team_image, old_team_image)
    elif team_prompt:
        team["team_image"] = generate_gemini_image(
            build_image_prompt("team", team_prompt, team=team),
            subfolder="ai/team",
            aspect_ratio="1:1"
        ) or old_team_image
    else:
        team["team_image"] = old_team_image

    action = request.form.get("action", "add")
    member_id = request.form.get("member_id", type=int)
    name = request.form.get("name", "").strip()

    if action == "save_team":
        save_generated_team(team)
        return redirect(url_for("result"))

    if action == "back" and not name:
        save_generated_team(team)

        members = team.get("members", [])
        if members:
            last_member_id = members[-1].get("id")
            return redirect(url_for("input_page", member_id=last_member_id, flow="edit"))
        else:
            return redirect(url_for("input_page"))


    if action == "make" and not member_id and not name:
        save_generated_team(team)
        return redirect(url_for("result"))

    if not name:
        save_generated_team(team)
        return redirect(url_for("input_page"))

    profile_image = request.files.get("profile_image") or request.files.get("image")
    profile_ai_prompt = request.form.get("profile_ai_prompt", "").strip()
    github_id = request.form.get("github", "").strip()
    sns_id = request.form.get("sns", "").strip()

    github_url = f"https://github.com/{github_id}" if github_id else ""
    sns_url = f"https://instagram.com/{sns_id}" if sns_id else ""
    portfolio_link = request.form.get("portfolio_link", "").strip()
    portfolio_file = request.files.get("portfolio_file")
    portfolio_file_path, portfolio_file_name = save_uploaded_asset(
        portfolio_file,
        request.form.get("portfolio_file_path", "").strip(),
        request.form.get("portfolio_file_name", "").strip(),
        subfolder="portfolio",
        allowed_extensions=ALLOWED_PORTFOLIO_EXTENSIONS
    )

    portfolio = []
    portfolio_titles = request.form.getlist("portfolio_title")
    portfolio_starts = request.form.getlist("portfolio_start_date")
    portfolio_ends = request.form.getlist("portfolio_end_date")
    portfolio_roles = request.form.getlist("portfolio_role")
    portfolio_descs = request.form.getlist("portfolio_desc")

    for title, start, end, role, desc in zip(
        portfolio_titles,
        portfolio_starts,
        portfolio_ends,
        portfolio_roles,
        portfolio_descs
    ):
        title = title.strip()
        start = start.strip()
        end = end.strip()
        role = role.strip()
        desc = desc.strip()

        if title or start or end or role or desc:
            portfolio.append({
                "title": title,
                "period": f"{start} ~ {end}",
                "role": role,
                "desc": desc
            })

    languages = request.form.getlist("languages")

    language_etc = request.form.get("language_etc", "").strip()
    language_etc_checked = request.form.get("language_etc_check")

    if language_etc_checked and language_etc:
        languages.append(language_etc)

    member_data = {
        "name": name,
        "student_number": request.form.get("student_number", "").strip(),
        "major": request.form.get("major", "").strip(),
        "phone": request.form.get("phone", "").strip(),
        "email": request.form.get("email", "").strip(),
        "role": request.form.get("role", "").strip(),
        "languages": languages,
        "github": github_url,
        "sns": sns_url,
        "intro": request.form.get("intro", "").strip(),
        "portfolio_link": portfolio_link,
        "portfolio_file": portfolio_file_path,
        "portfolio_file_name": portfolio_file_name,
        "portfolio": portfolio
    }

    if member_id:
        for idx, member in enumerate(team.get("members", [])):
            if int(member.get("id")) == member_id:
                old_image = member.get("image", "images/default.png")

                member_data["id"] = member_id
                if profile_image and profile_image.filename:
                    member_data["image"] = save_uploaded_file(profile_image, old_image)
                elif profile_ai_prompt:
                    member_data["image"] = generate_gemini_image(
                        build_image_prompt("profile", profile_ai_prompt, team=team, member=member_data),
                        subfolder="ai/profile",
                        aspect_ratio="1:1"
                    ) or old_image
                else:
                    member_data["image"] = old_image

                team["members"][idx] = member_data
                save_generated_team(team)

                flow = request.form.get("flow", "")

                if flow == "edit":
                    if action == "previous" and idx > 0:
                        previous_member_id = team["members"][idx - 1]["id"]
                        return redirect(url_for("input_page", member_id=previous_member_id, flow="edit"))

                    if action == "add_member" and len(team["members"]) < 4:
                        return redirect(url_for("input_page"))

                    if action == "save_result":
                        return redirect(url_for("result"))

                    if idx + 1 < len(team["members"]):
                        next_member_id = team["members"][idx + 1]["id"]
                        return redirect(url_for("input_page", member_id=next_member_id, flow="edit"))
                    else:
                        return redirect(url_for("result"))
                else:
                    return redirect(url_for("member_detail", member_id=member_id))

        abort(404)

    if len(team.get("members", [])) >= 4:
        save_generated_team(team)
        return redirect(url_for("input_page"))

    new_id = team.get("next_member_id", 1000)
    team["next_member_id"] = new_id + 1

    member_data["id"] = new_id
    if profile_image and profile_image.filename:
        member_data["image"] = save_uploaded_file(profile_image, "images/default.png")
    elif profile_ai_prompt:
        member_data["image"] = generate_gemini_image(
            build_image_prompt("profile", profile_ai_prompt, team=team, member=member_data),
            subfolder="ai/profile",
            aspect_ratio="1:1"
        ) or "images/default.png"
    else:
        member_data["image"] = "images/default.png"

    team["members"].append(member_data)
    save_generated_team(team)

    if action == "back":
        previous_member = team["members"][-2] if len(team["members"]) > 1 else member_data
        return redirect(url_for("input_page", member_id=previous_member["id"], flow="edit"))

    if action == "make":
        return redirect(url_for("result"))

    return redirect(url_for("input_page"))

@app.route("/result")
def result():
    team = get_generated_team()

    return render_template(
        "result.html",
        team=team,
        members=team.get("members", [])
    )


@app.route("/members/<int:member_id>")
def member_detail(member_id):
    root_member = get_root_member_by_id(member_id)

    if root_member:
        return render_template(
            "member_detail.html",
            member=root_member,
            is_root_member=True
        )

    generated_member = get_generated_member_by_id(member_id)

    if generated_member:
        return render_template(
            "member_detail.html",
            member=generated_member,
            is_root_member=False
        )

    abort(404)

@app.route("/members/<int:member_id>/delete", methods=["POST"])
def delete_generated_member(member_id):
    team = get_generated_team()
    members = team.get("members", [])
    remaining_members = [
        member
        for member in members
        if int(member.get("id")) != member_id
    ]

    if len(remaining_members) == len(members):
        abort(404)

    team["members"] = remaining_members
    save_generated_team(team)
    return redirect(url_for("result"))

@app.route("/contact")
def contact():
    members = load_root_members()

    return render_template(
        "contact.html",
        members=members
    )

def read_json_file(path, default=None):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return [] if default is None else default


def write_json_file(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def ensure_board_runtime_file(runtime_path):
    if os.path.exists(runtime_path):
        return

    write_json_file(runtime_path, [])


def with_board_source(items, source):
    sourced_items = []

    for item in items:
        sourced_item = dict(item)
        sourced_item["_source"] = source
        sourced_items.append(sourced_item)

    return sourced_items


def merge_seed_and_runtime(seed_path, runtime_path):
    ensure_board_runtime_file(runtime_path)

    seed_items = read_json_file(seed_path, [])
    runtime_items = read_json_file(runtime_path, [])
    seed_ids = {item.get("id") for item in seed_items}
    user_items = [
        item
        for item in runtime_items
        if item.get("id") not in seed_ids
    ]

    return with_board_source(seed_items, "seed") + with_board_source(user_items, "runtime")


def get_posts():
    return merge_seed_and_runtime(POSTS_SEED_FILE, POSTS_RUNTIME_FILE)


def save_posts(posts):
    runtime_posts = [
        {key: value for key, value in post.items() if key != "_source"}
        for post in posts
        if post.get("_source") != "seed"
    ]
    write_json_file(POSTS_RUNTIME_FILE, runtime_posts)


def get_comments():
    return merge_seed_and_runtime(COMMENTS_SEED_FILE, COMMENTS_RUNTIME_FILE)


def save_comments(comments):
    runtime_comments = [
        {key: value for key, value in comment.items() if key != "_source"}
        for comment in comments
        if comment.get("_source") != "seed"
    ]
    write_json_file(COMMENTS_RUNTIME_FILE, runtime_comments)

@app.route('/board')
def board_list():
    posts = get_posts() 
    posts.reverse()
    return render_template('board/post_list.html', posts=posts)

@app.route('/board/write')
def board_write():
    return render_template('board/post_form.html', post=None)

@app.route('/board/<int:post_id>')
def board_detail(post_id):
    posts = get_posts()
    
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post: abort(404)

    curr_idx = posts.index(post)
    prev_post = posts[curr_idx - 1] if curr_idx > 0 else None
    next_post = posts[curr_idx + 1] if curr_idx < len(posts) - 1 else None

    all_comments = get_comments()
    
    post_comments = [c for c in all_comments if c['post_id'] == post_id]

    return render_template('board/post_detail.html', 
                           post=post, prev_id=prev_post['id'] if prev_post else None,
                           next_id=next_post['id'] if next_post else None,
                           comments=post_comments)

@app.route('/board/<int:post_id>/edit')
def board_edit(post_id):
    posts = get_posts()
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post: abort(404)
    return render_template('board/post_form.html', post=post)

@app.route('/board/update', methods=['POST'])
def board_update():
    action = request.form.get('action', 'add')
    post_id = request.form.get('post_id', type=int)
    input_pw = request.form.get('password', '').strip()
    current_time = datetime.now().strftime("%Y.%m.%d %H:%M")

    posts = get_posts()

    if action == 'add':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        content = request.form.get('content', '').strip()

        if not all([title, author, input_pw, content]):
            return "<script>alert('모든 항목을 입력해야 합니다.'); history.back();</script>"
        if not (input_pw.isdigit() and len(input_pw) == 4):
            return "<script>alert('비밀번호는 숫자 4자리여야 합니다.'); history.back();</script>"

        new_post = {
            "id": max([post['id'] for post in posts], default=0) + 1,
            "title": title, "author": author, "password": input_pw,
            "content": content, "date": current_time, "_source": "runtime"
        }
        posts.append(new_post)
        save_posts(posts)
        return redirect('/board')

    post = next((p for p in posts if p['id'] == post_id), None)
    if not post: abort(404)

    if str(input_pw) != str(post['password']):
        return "<script>alert('비밀번호가 일치하지 않습니다.'); history.back();</script>"

    if action == 'edit':
        new_title = request.form.get('title', '').strip()
        new_content = request.form.get('content', '').strip()
        if not new_title or not new_content:
            return "<script>alert('제목과 내용을 모두 입력해주세요.'); history.back();</script>"

        post['title'] = new_title
        post['content'] = new_content
        post['date'] = current_time
        save_posts(posts)
        return redirect(f'/board/{post_id}')

    elif action == 'delete':
        posts.remove(post)
        save_posts(posts)

        all_comments = get_comments()
        filtered_comments = [c for c in all_comments if c['post_id'] != post_id]
        save_comments(filtered_comments)

        return redirect('/board')

@app.route('/comments/<int:comment_id>/edit')
def comment_edit_view(comment_id):
    comments = get_comments()
    comment = next((c for c in comments if c['id'] == comment_id), None)
    if not comment: abort(404)
    return redirect(url_for('board_detail', post_id=comment['post_id'], edit_comment_id=comment_id) + f"#comment-{comment_id}")

@app.route('/comment/update', methods=['POST'])
def comment_update():
    action = request.form.get('action', 'add')
    post_id = request.form.get('post_id', type=int)
    comment_id = request.form.get('comment_id', type=int)
    input_pw = request.form.get('password', '').strip()
    current_time = datetime.now().strftime("%Y.%m.%d %H:%M")

    comments = get_comments()

    if action == 'add':
        author = request.form.get('author', '').strip()
        content = request.form.get('content', '').strip()
        if not all([author, input_pw, content]):
            return "<script>alert('모든 항목을 입력해주세요.'); history.back();</script>"

        new_comment = {
            "id": int(datetime.now().timestamp() * 1000), "post_id": post_id,
            "author": author, "password": input_pw, "content": content,
            "date": current_time, "_source": "runtime"
        }
        comments.append(new_comment)
        save_comments(comments)
        return redirect(f'/board/{post_id}')

    comment = next((c for c in comments if c['id'] == comment_id), None)
    if not comment: abort(404)

    if str(input_pw) != str(comment['password']):
        return "<script>alert('비밀번호가 틀렸습니다.'); history.back();</script>"

    if action == 'edit':
        comment['author'] = request.form.get('author', '').strip()
        comment['content'] = request.form.get('content', '').strip()
        comment['date'] = current_time
        save_comments(comments)
        return redirect(f'/board/{comment["post_id"]}#comment-{comment_id}')

    elif action == 'delete':
        target_post_id = comment['post_id']
        comments.remove(comment)
        save_comments(comments)
        return redirect(f'/board/{target_post_id}')


if __name__ == "__main__":
    app.run(debug=True)
