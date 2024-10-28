import json
from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)


@app.route('/')
def home():
    # fetch the blog posts from the JSON file
    with open("file_path", "r") as file:
        blog_posts = json.load(file)

    # render the index.html template and pass the posts to it
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        # Get form data
        new_post = {
            'id': None,  # Will be assigned later
            'author': request.form['author'],
            'title': request.form['title'],
            'content': request.form['content']
        }

        # Load existing posts
        try:
            with open('path/to/blog_posts.json', 'r') as file:
                blog_posts = json.load(file)
        except FileNotFoundError:
            blog_posts = []  # If the file doesn't exist, create an empty list

        # Assign an ID to the new post (incrementing the last post's ID)
        if blog_posts:
            new_post['id'] = blog_posts[-1]['id'] + 1
        else:
            new_post['id'] = 1

        # Add the new post to the list
        blog_posts.append(new_post)

        # Save the updated posts back to the JSON file
        with open('path/to/blog_posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

        # Redirect to the index page after adding the post
        return redirect(url_for('home'))

    return render_template('create_post.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    # Load the existing posts from the JSON file
    with open('path/to/blog_posts.json', 'r') as file:
        blog_posts = json.load(file)

    # Filter out the post with the given post_id
    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    # Save the updated list back to the JSON file
    with open('path/to/blog_posts.json', 'w') as file:
        json.dump(blog_posts, file, indent=4)

    # Redirect back to the index page
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)