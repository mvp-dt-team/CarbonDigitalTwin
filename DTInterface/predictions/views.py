from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.urls import reverse

from .forms import AddBlockForm
import requests
import json

URL_DATA_STORAGE = "http://127.0.0.1:3000"
API_GET_SENSORS_ITEM = "sensor/?need_active=true"
API_GET_PROPERTIES = "blocks/property"
API_BLOCK = "blocks"
API_ADD_BLOCK_PARAMS = "blocks/models/params"
API_PREDICTIONS = "blocks/prediction"


def get_sensors() -> list:
    return json.loads(requests.get(f"{URL_DATA_STORAGE}/{API_GET_SENSORS_ITEM}").text)


def get_properties() -> list:
    return json.loads(requests.get(f"{URL_DATA_STORAGE}/{API_GET_PROPERTIES}").text)


def find_sensors_with_measurements(block_data):
    sensors_data = get_sensors()

    # Создаем словарь для быстрого доступа к датчикам по их id
    sensor_dict = {sensor["id"]: sensor for sensor in sensors_data}

    # Инициализируем список для хранения результатов
    result = []

    # Итерируемся по датчикам в данных блока
    for sensor in block_data.get("sensors", []):
        sensor_item_id = sensor.get("sensor_item_id")
        measurement_source_id = sensor.get("measurement_source_id")

        # Ищем датчик по sensor_item_id и measurement_source_id
        for sensor_id, sensor_info in sensor_dict.items():
            for prop in sensor_info["properties"]:
                if (
                    prop["measurement_source_id"] == measurement_source_id
                    and sensor_id == sensor_item_id
                ):
                    result.append(
                        {
                            "id": sensor_id,
                            "measurement_source_id": measurement_source_id,
                            "name": prop["name"],
                            "description": sensor_info["description"],
                            "sensor_model_id": sensor_info["sensor_model_id"],
                            "unit": prop["unit"],
                        }
                    )

    return result


def management_panel(request, block_id):
    blocks = json.loads(
        requests.get(f"{URL_DATA_STORAGE}/{API_BLOCK}/?need_active=false").content
    )
    current_block = None
    sensors_data = get_sensors()
    for block in blocks:
        if block.get("id") == block_id:
            current_block = block
            break

    sensors = find_sensors_with_measurements(block)

    context = {"block": block, "sensors": sensors}
    return render(request, "management_panel.html", context=context)


def toggle_block(request, block_id):
    requests.patch(f"{URL_DATA_STORAGE}/{API_BLOCK}/{block_id}")
    return HttpResponseRedirect(reverse("management_panel", args=(block_id,)))


def get_predictions(request, block_id, n_predictions):
    return JsonResponse(
        json.loads(
            requests.get(
                f"{URL_DATA_STORAGE}/{API_PREDICTIONS}?block_id={block_id}&n_predictions={n_predictions}"
            ).text
        ),
        safe=False,
    )


def block_list(request):
    blocks = json.loads(
        requests.get(f"{URL_DATA_STORAGE}/{API_BLOCK}/?need_active=false").content
    )
    context = {"title": "Список блоков", "blocks": blocks}
    return render(request, "block_list.html", context=context)


def add_block(request):
    sensors_data = get_sensors()
    properties_data = get_properties()

    sensors = [
        (f"{sensor['id']} {prop['measurement_source_id']}", prop["name"])
        for sensor in sensors_data
        for prop in sensor["properties"]
    ]
    properties = [(prop["id"], prop["name"]) for prop in properties_data]

    context = {"title": "Добавление блоков"}

    if request.method == "POST":
        form = AddBlockForm(request.POST, request.FILES)
        form.fields["sensors"].choices = sensors
        form.fields["properties"].choices = properties
        # print(form.sensors)
        if form.is_valid():
            print(json.dumps({"name": form.cleaned_data["blockname"]}))
            response_api = requests.post(
                f"{URL_DATA_STORAGE}/{API_BLOCK}",
                json={"name": form.cleaned_data["blockname"]},
            )
            print(response_api)
            if response_api.status_code == 200:
                name = form.cleaned_data["model_name"]
                description = form.cleaned_data["model_description"]
                type_model = form.cleaned_data["model_type"]
                block_id = json.loads(response_api.text)["id"]
                file = form.cleaned_data["model_file"]
                selected_sensors = form.cleaned_data["sensors"]
                selected_properties = form.cleaned_data["properties"]
                print(selected_sensors)
                print(selected_properties)
                params = {
                    "measurement_source_ids": [
                        int(x.split()[1]) for x in selected_sensors
                    ],
                    "sensor_item_ids": [int(x.split()[0]) for x in selected_sensors],
                    "properties_ids": [int(x) for x in selected_properties],
                }
                files = {"file": (file.name, file.read(), file.content_type)}
                data = {
                    "name": name,
                    "description": description,
                    "type_model": type_model,
                    "block_id": block_id,
                }

                response = requests.post(
                    f"{URL_DATA_STORAGE}/{API_ADD_BLOCK_PARAMS}",
                    params=params,
                    files=files,
                    data=data,
                )

                if response.status_code == 200:
                    return HttpResponseRedirect(reverse("block_list"))
                else:
                    # Обработка ошибок
                    print(response.status_code)
                    print(response.json())
        else:
            print(form.errors)
    else:
        form = AddBlockForm()
        if len(sensors) < 1:
            sensors.append(("None", "Ничего нет"))
        if len(properties) < 1:
            properties.append(("None", "Ничего нет"))
        print(sensors_data)
        print(properties_data)
        form.fields["sensors"].choices = sensors
        form.fields["properties"].choices = properties

    return render(
        request,
        "add_block_form.html",
        {"form": form, "name_form": "Добавление нового блока"},
    )
