from ultralytics import YOLO

# Load a pretrained YOLOv8n model
model = YOLO("YOLO8s_best.pt")

# Define path to the image file
sources = [
    "test/test1.jpg",
    "test/test2.jpg",
    "test/test3.jpg",
    "test/test4.jpg",
    "test/test5.jpg",
    "test/test6.jpg",
    "test/test7.jpg",
    "test/test8.jpg",
    "test/test9.jpg",
    "test/test10.jpg",
]

for item in sources:
    # Run inference on the source
    results = model(item)  # list of Results objects
    print(results[0].speed)
    # with open('result.txt', 'a', encoding='utf8') as file:
    #     file.write('\n\n\n\n')
    #     file.write(item)
    #     file.write(str(results))
