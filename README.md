# Hearth Card API

Documentation @ http://docs.hearthstone.apiary.io/#


## Setup

#### Extract XML data from Unity file

- Get the latest cardxml10.unity3d file from your Hearthstone directory.

```bash
disunity extract cardxml0.unity3d
```

#### Convert XML data to JSON

```bash
python xml_to_json.py
```

#### Start MongoDB
```bash
mongod
```

#### Persist data and complete setup
```bash
python setup.py
```
