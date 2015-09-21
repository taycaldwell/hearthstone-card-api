# Hearth Card API

Documentation @ http://docs.hearthstone.apiary.io/#


## Dependencies

- [Python 2.7](https://www.python.org/download/releases/2.7/)

- [DisUnity](https://github.com/ata4/disunity)

- [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/bs4/doc/)


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
