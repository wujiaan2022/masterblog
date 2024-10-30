import json
from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)


@app.route('/')
def home():
    # fetch the blog posts from the JSON file
    with open("masterblog/blog_posts.json", "r") as file:
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
            with open('masterblog/blog_posts.json', 'r') as file:
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
        with open('masterblog/blog_posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

        # Redirect to the index page after adding the post
        return redirect(url_for('home'))

    return render_template('create_post.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    # Load the existing posts from the JSON file
    with open('masterblog/blog_posts.json', 'r') as file:
        blog_posts = json.load(file)

    # Filter out the post with the given post_id
    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    # Save the updated list back to the JSON file
    with open('masterblog/blog_posts.json', 'w') as file:
        json.dump(blog_posts, file, indent=4)

    # Redirect back to the index page
    return redirect(url_for('home'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    # Load existing posts from the JSON file
    with open('masterblog/blog_posts.json', 'r') as file:
        blog_posts = json.load(file)

    # Find the post to update
    post = next((p for p in blog_posts if p['id'] == post_id), None)

    if not post:
        return "Post not found", 404  # Handle the case if the post does not exist

    if request.method == 'POST':
        # Update post with form data
        post['title'] = request.form['title']
        post['author'] = request.form['author']
        post['content'] = request.form['content']

        # Save the updated posts back to the JSON file
        with open('path/to/blog_posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

        # Redirect to the main page or specific post page
        return redirect(url_for('home'))

    # Render the update form with current post data if it's a GET request
    return render_template('update_post.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)