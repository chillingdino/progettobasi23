from flask import Flask, request, url_for, redirect, render_template
from py.create import *

app = create_app()

if __name__ == '__main__':
	app.run(debug=True)