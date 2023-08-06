import os

def launch_mistic():
	os.system('bokeh serve --port 50947 --show image_tSNE_GUI')

def rem_hidden_files():
	os.system('find . | grep .git | xargs rm -rf')
