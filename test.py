from PIL import Image

# Open your PNG
img = Image.open('icons/app/icon.png')

# Define sizes (common for Windows ICOs)
sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]

# Save as multi-resolution ICO
img.save("Kryypto-icon.ico", sizes=sizes)
