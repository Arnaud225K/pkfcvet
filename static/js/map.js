// Яндекс Карты "География поставок"
ymaps.ready(init);
function init() {

    var geoMap = new ymaps.Map('map', {
        center: [60.698653, 79.505405],
        type: "yandex#map",
        zoom: 3,
        controls: ["typeSelector", "zoomControl"]
    });
    //geoMap.controls.add('zoomControl');
    geoMap.behaviors.disable('scrollZoom');

    // Абакан
    var myPlacemark1 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [53.705300, 91.374500]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "655004, Республика Хакасия, г. Абакан, ул. Заводская, д. 1в",
            balloonContentHeader: "г. Абакан",
            balloonContentBody: "655004, Республика Хакасия, г. Абакан, ул. Заводская, д. 1в"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Абакан

    // Архангельск
    var myPlacemark2 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [64.592400, 40.610400]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "163045, г. Архангельск, Талажское ш., д. 45",
            balloonContentHeader: "г. Архангельск",
            balloonContentBody: "163045, г. Архангельск, Талажское ш., д. 45"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Архангельск

    // Астрахань
    var myPlacemark3 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [46.541900, 48.321800]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "416474, г. Астрахань, Приволжский р-н, Кулаковский промузел, ш. Энергетиков, д. 5а",
            balloonContentHeader: "г. Астрахань",
            balloonContentBody: "416474, г. Астрахань, Приволжский р-н, Кулаковский промузел, ш. Энергетиков, д. 5а"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Астрахань

    // Барнаул
    var myPlacemark4 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [53.322900, 83.638800]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "656922, г. Барнаул, ул. Попова, д. 244",
            balloonContentHeader: "г. Барнаул",
            balloonContentBody: "656922, г. Барнаул, ул. Попова, д. 244"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Барнаул

    // Белгород
    var myPlacemark5 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [50.563700, 36.653800]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "308013, г. Белгород, ул. Коммунальная, д. 18",
            balloonContentHeader: "г. Белгород",
            balloonContentBody: "308013, г. Белгород, ул. Коммунальная, д. 18"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Белгород

    // Благовещенск
    var myPlacemark6 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [50.298100, 127.55500]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "675000, г. Благовещенск, ул. Раздольная, д. 33",
            balloonContentHeader: "г. Благовещенск",
            balloonContentBody: "675000, г. Благовещенск, ул. Раздольная, д. 33"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Благовещенск

    // Брянск
    var myPlacemark7 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [53.297000, 34.319900]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "241035, г. Брянск, ул. Бурова, д. 20",
            balloonContentHeader: "г. Брянск",
            balloonContentBody: "241035, г. Брянск, ул. Бурова, д. 20"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Брянск

    // Великий Новгород
    var myPlacemark8 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [58.557300, 31.27200]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "173008, г. Великий Новгород, ул. Большая Санкт-Петербургская, д. 85/1",
            balloonContentHeader: "г. Великий Новгород",
            balloonContentBody: "173008, г. Великий Новгород, ул. Большая Санкт-Петербургская, д. 85/1"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Великий Новгород

    // Владивосток
    var myPlacemark9 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [43.165700, 131.92600]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "690049, г. Владивосток, ул. Бородинская, д. 18б",
            balloonContentHeader: "г. Владивосток",
            balloonContentBody: "690049, г. Владивосток, ул. Бородинская, д. 18б"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Владивосток

    // Владимир
    var myPlacemark10 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [56.160200, 40.382100]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "600035, г. Владимир, ул. Куйбышева, д. 4",
            balloonContentHeader: "г. Владимир",
            balloonContentBody: "600035, г. Владимир, ул. Куйбышева, д. 4"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Владимир

    // Волгоград
    var myPlacemark11 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [48.764300, 44.457600]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "400075, г. Волгоград, Проезд Мирный, д. 6",
            balloonContentHeader: "г. Волгоград",
            balloonContentBody: "400075, г. Волгоград, Проезд Мирный, д. 6"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Волгоград

    // Вологда
    var myPlacemark12 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [59.207900, 39.819900]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "400075, г. Волгоград, Проезд Мирный, д. 6",
            balloonContentHeader: "г. Вологда",
            balloonContentBody: "400075, г. Волгоград, Проезд Мирный, д. 6"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Вологда

    // Воронеж
    var myPlacemark13 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [51.675800, 39.152700]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "394019, г. Воронеж, ул. Торпедо, д. 45в",
            balloonContentHeader: "г. Воронеж",
            balloonContentBody: "394019, г. Воронеж, ул. Торпедо, д. 45в"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Воронеж

    // Екатеринбург
    var myPlacemark14 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [56.90800, 60.630500]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "620057, г. Екатеринбург, ул. Таганская, д. 60",
            balloonContentHeader: "г. Екатеринбург",
            balloonContentBody: "620057, г. Екатеринбург, ул. Таганская, д. 60"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Екатеринбург

    // Иваново
    var myPlacemark15 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [56.99100, 40.908200]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "153031, г. Иваново, ул. Суздальская, д. 16а",
            balloonContentHeader: "г. Иваново",
            balloonContentBody: "153031, г. Иваново, ул. Суздальская, д. 16а"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Иваново

    // Ижевск
    var myPlacemark16 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [56.815300, 53.203600]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "426028, Удмуртская республика, г. Ижевск, ул. Маяковского, д. 35",
            balloonContentHeader: "г. Ижевск",
            balloonContentBody: "426028, Удмуртская республика, г. Ижевск, ул. Маяковского, д. 35"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Ижевск

    // Иркутск
    var myPlacemark17 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [52.326200, 104.25600]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "664020, г. Иркутск, ул. Трактовая, д. 24/21",
            balloonContentHeader: "г. Иркутск",
            balloonContentBody: "664020, г. Иркутск, ул. Трактовая, д. 24/21"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Иркутск

    // Йошкар-Ола
    var myPlacemark18 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [56.371300, 47.523400]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "424006, Республика Марий Эл, г. Йошкар-Ола, ул. Соловьева, д. 18",
            balloonContentHeader: "г. Йошкар-Ола",
            balloonContentBody: "424006, Республика Марий Эл, г. Йошкар-Ола, ул. Соловьева, д. 18"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Йошкар-Ола

    // Казань
    var myPlacemark19 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [55.775300, 49.188800]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "420073, Республика Татарстан, г. Казань, ул. Аделя Кутуя, д. 151",
            balloonContentHeader: "г. Казань",
            balloonContentBody: "420073, Республика Татарстан, г. Казань, ул. Аделя Кутуя, д. 151"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Казань

    // Калининград
    var myPlacemark20 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [54.669700, 20.535600]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "236034, г. Калининград, ул. Дзержинского, д. 168",
            balloonContentHeader: "г. Калининград",
            balloonContentBody: "236034, г. Калининград, ул. Дзержинского, д. 168"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Калининград

    // Калуга
    var myPlacemark21 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [54.548800, 36.333300]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "248000, г. Калуга, Грабцевское ш., д. 99",
            balloonContentHeader: "г. Калуга",
            balloonContentBody: "248000, г. Калуга, Грабцевское ш., д. 99"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Калуга

    // Кемерово
    var myPlacemark22 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [55.308800, 86.1400]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "650070, г. Кемерово, ул. Тухачевского, д. 60",
            balloonContentHeader: "г. Кемерово",
            balloonContentBody: "650070, г. Кемерово, ул. Тухачевского, д. 60"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Кемерово

    // Киров
    var myPlacemark23 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [58.578100, 49.59500]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "610014, г. Киров, ул. Щорса, д. 105",
            balloonContentHeader: "г. Киров",
            balloonContentBody: "610014, г. Киров, ул. Щорса, д. 105"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Киров

    // Кострома
    var myPlacemark24 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [57.761034, 40.985168]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "156019, г. Кострома, ул. Локомотивная, д. 6ж",
            balloonContentHeader: "г. Кострома",
            balloonContentBody: "156019, г. Кострома, ул. Локомотивная, д. 6ж"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Кострома

    // Краснодар
    var myPlacemark25 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [45.080800, 38.989900]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "350001, г. Краснодар, ул. А. Покрышкина, д. 2/4",
            balloonContentHeader: "г. Краснодар",
            balloonContentBody: "350001, г. Краснодар, ул. А. Покрышкина, д. 2/4"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Краснодар

    // Красноярск
    var myPlacemark26 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [56.075600, 92.928900]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "660020, г. Красноярск, Северное ш., д. 17",
            balloonContentHeader: "г. Красноярск",
            balloonContentBody: "660020, г. Красноярск, Северное ш., д. 17"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Красноярск

    // Курган
    var myPlacemark27 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [55.478600, 65.378900]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "640007, г. Курган, ул. Омская, д. 146",
            balloonContentHeader: "г. Курган",
            balloonContentBody: "640007, г. Курган, ул. Омская, д. 146"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Курган

    // Курск
    var myPlacemark28 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [51.703025, 36.169614]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "305023, г. Курск, ул. Литовская, д. 12а",
            balloonContentHeader: "г. Курск",
            balloonContentBody: "305023, г. Курск, ул. Литовская, д. 12а"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Курск

    // Липецк
    var myPlacemark29 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [52.627900, 39.527100]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "398037, г. Липецк, Трубный проезд, стр. 6",
            balloonContentHeader: "г. Липецк",
            balloonContentBody: "398037, г. Липецк, Трубный проезд, стр. 6"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Липецк

    // Мурманск
    var myPlacemark30 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [68.995700, 33.124300]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "183034, г. Мурманск, ул. Домостроительная, д. 8",
            balloonContentHeader: "г. Мурманск",
            balloonContentBody: "183034, г. Мурманск, ул. Домостроительная, д. 8"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Мурманск

    // Нижний Новгород
    var myPlacemark31 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [56.294300, 43.885300]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "603034, г. Нижний Новгород, ул. Удмуртская д. 38, склад № 7",
            balloonContentHeader: "г. Нижний Новгород",
            balloonContentBody: "603034, г. Нижний Новгород, ул. Удмуртская д. 38, склад № 7"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Нижний Новгород

    // Новый Уренгой
    var myPlacemark32 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [66.092402, 76.696407]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "629307, г. Новый Уренгой, ул. Индустриальная, д. 14",
            balloonContentHeader: "г. Новый Уренгой",
            balloonContentBody: "629307, г. Новый Уренгой, ул. Индустриальная, д. 14"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Новый Уренгой

    // Новосибирск
    var myPlacemark33 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [54.944300, 82.925400]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "630119, г. Новосибирск, ул. Петухова, д. 79, к. 3",
            balloonContentHeader: "г. Новосибирск",
            balloonContentBody: "630119, г. Новосибирск, ул. Петухова, д. 79, к. 3"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Новосибирск

    // Омск
    var myPlacemark34 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [54.979400, 73.448800]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "644027, г. Омск, ул. 20 лет РККА, д. 302а",
            balloonContentHeader: "г. Омск",
            balloonContentBody: "644027, г. Омск, ул. 20 лет РККА, д. 302а"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Омск

    // Орел
    var myPlacemark35 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [52.931900, 36.073500]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "302024, г. Орел, ул. Поселковая, д. 15",
            balloonContentHeader: "г. Орел",
            balloonContentBody: "302024, г. Орел, ул. Поселковая, д. 15"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Орел

    // Оренбург
    var myPlacemark36 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [51.710900, 55.110800]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "460034, г. Оренбург, ул. Центральная, д. 1",
            balloonContentHeader: "г. Оренбург",
            balloonContentBody: "460034, г. Оренбург, ул. Центральная, д. 1"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Оренбург

    // Пенза
    var myPlacemark37 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [53.199400, 45.020100]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "440032, г. Пенза, ул. Дорожная, д. 10",
            balloonContentHeader: "г. Пенза",
            balloonContentBody: "440032, г. Пенза, ул. Дорожная, д. 10"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Пенза

    // Пермь
    var myPlacemark38 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [58.032500, 56.141600]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "614031, г. Пермь, ул. Докучаева, д. 50",
            balloonContentHeader: "г. Пермь",
            balloonContentBody: "614031, г. Пермь, ул. Докучаева, д. 50"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Пермь

    // Петрозаводск
    var myPlacemark39 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [61.774100, 34.402600]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "185005, Республика Карелия, г. Петрозаводск, ул.Коммунистов, д. 50",
            balloonContentHeader: "г. Петрозаводск",
            balloonContentBody: "185005, Республика Карелия, г. Петрозаводск, ул.Коммунистов, д. 50"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Петрозаводск

    // Псков
    var myPlacemark40 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [57.834300, 28.311300]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "180006, г. Псков, ул. Леона Поземского, д. 110д",
            balloonContentHeader: "г. Псков",
            balloonContentBody: "180006, г. Псков, ул. Леона Поземского, д. 110д"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Псков

    // Ростов-на-Дону
    var myPlacemark41 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [47.191700, 39.634800]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "344033, г. Ростов-на-Дону, ул. Портовая, д. 543",
            balloonContentHeader: "г. Ростов-на-Дону",
            balloonContentBody: "344033, г. Ростов-на-Дону, ул. Портовая, д. 543"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Ростов-на-Дону

    // Рязань
    var myPlacemark42 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [54.386200, 39.381200]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "390020, г. Рязань, Окружная дорога, 185 км, стр. 6а",
            balloonContentHeader: "г. Рязань",
            balloonContentBody: "390020, г. Рязань, Окружная дорога, 185 км, стр. 6а"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Рязань

    // Самара
    var myPlacemark43 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [53.271700, 50.225300]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "443031, г. Самара, ул. Демократическая, д. 45а",
            balloonContentHeader: "г. Самара",
            balloonContentBody: "443031, г. Самара, ул. Демократическая, д. 45а"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Самара

    // Санкт-Петербург
    var myPlacemark44 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [59.8400, 30.295900]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "196240, г. Санкт-Петербург, ул. Кубинская, д. 75",
            balloonContentHeader: "г. Санкт-Петербург",
            balloonContentBody: "196240, г. Санкт-Петербург, ул. Кубинская, д. 75"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Санкт-Петербург

    // Саранск
    var myPlacemark45 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [54.204700, 45.225100]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "430009, Республика Мордовия, г. Саранск, ул. Краснофлотская, д. 107а",
            balloonContentHeader: "г. Саранск",
            balloonContentBody: "430009, Республика Мордовия, г. Саранск, ул. Краснофлотская, д. 107а"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Саранск

    // Саратов
    var myPlacemark46 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [51.485640, 45.919685]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "410039, г. Саратов, Крымский проезд, д. 7",
            balloonContentHeader: "г. Саратов",
            balloonContentBody: "410039, г. Саратов, Крымский проезд, д. 7"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Саратов

    // Смоленск
    var myPlacemark47 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [54.796200, 32.026100]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "214012, г. Смоленск, ул. Кашена, д. 23",
            balloonContentHeader: "г. Смоленск",
            balloonContentBody: "214012, г. Смоленск, ул. Кашена, д. 23"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Смоленск

    // Сочи
    var myPlacemark48 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [43.609300, 39.727700]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "354065, г. Сочи, ул. Гагарина, д. 61/2",
            balloonContentHeader: "г. Сочи",
            balloonContentBody: "354065, г. Сочи, ул. Гагарина, д. 61/2"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Сочи

    // Ставрополь
    var myPlacemark49 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [45.066600, 41.933200]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "355035, г. Ставрополь, ул. Буйнакского, д. 35",
            balloonContentHeader: "г. Ставрополь",
            balloonContentBody: "355035, г. Ставрополь, ул. Буйнакского, д. 35"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Ставрополь

    // Сыктывкар
    var myPlacemark50 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [61.68300, 50.793500]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "167031, Республика Коми, г. Сыктывкар, ул. Печорская, д. 67",
            balloonContentHeader: "г. Сыктывкар",
            balloonContentBody: "167031, Республика Коми, г. Сыктывкар, ул. Печорская, д. 67"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Сыктывкар

    // Тамбов
    var myPlacemark51 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [52.698400, 41.425800]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "392022, г. Тамбов, ул. Академика Островитянова, д. 9б",
            balloonContentHeader: "г. Тамбов",
            balloonContentBody: "392022, г. Тамбов, ул. Академика Островитянова, д. 9б"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Тамбов

    // Тверь
    var myPlacemark52 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [56.829300, 35.919100]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "170028, г. Тверь, ул. Коминтерна, д. 91/14",
            balloonContentHeader: "г. Тверь",
            balloonContentBody: "170028, г. Тверь, ул. Коминтерна, д. 91/14"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Тверь

    // Томск
    var myPlacemark53 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [56.520800, 84.925500]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "634009, г. Томск, ул. Нижнелуговая, д. 89а",
            balloonContentHeader: "г. Томск",
            balloonContentBody: "634009, г. Томск, ул. Нижнелуговая, д. 89а"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Томск

    // Тула
    var myPlacemark54 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [54.184767, 37.549920]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "300024, г. Тула, Ханинский проезд, д. 29",
            balloonContentHeader: "г. Тула",
            balloonContentBody: "300024, г. Тула, Ханинский проезд, д. 29"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Тула

    // Тюмень
    var myPlacemark55 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [57.12300, 65.57800]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "625016, г. Тюмень, ул. 30 лет Победы, д. 35, стр. 2",
            balloonContentHeader: "г. Тюмень",
            balloonContentBody: "625016, г. Тюмень, ул. 30 лет Победы, д. 35, стр. 2"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Тюмень

    // Улан-Удэ
    var myPlacemark56 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [51.835100, 107.59700]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "670047, Республика Бурятия, г. Улан-Удэ, ул. Сахьяновой, д. 9, стр. 18",
            balloonContentHeader: "г. Улан-Удэ",
            balloonContentBody: "670047, Республика Бурятия, г. Улан-Удэ, ул. Сахьяновой, д. 9, стр. 18"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Улан-Удэ

    // Ульяновск
    var myPlacemark57 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [54.256900, 48.255600]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "670047, Республика Бурятия, г. Улан-Удэ, ул. Сахьяновой, д. 9, стр. 18",
            balloonContentHeader: "г. Ульяновск",
            balloonContentBody: "670047, Республика Бурятия, г. Улан-Удэ, ул. Сахьяновой, д. 9, стр. 18"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Ульяновск

    // Уфа
    var myPlacemark58 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [54.796700, 56.060600]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "450027, Республика Башкортостан, г. Уфа, ул. Трамвайная, д. 2",
            balloonContentHeader: "г. Уфа",
            balloonContentBody: "450027, Республика Башкортостан, г. Уфа, ул. Трамвайная, д. 2"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Уфа

    // Хабаровск
    var myPlacemark59 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [48.449700, 135.13500]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "680032, г. Хабаровск, ул. Зеленая, д. 3а",
            balloonContentHeader: "г. Хабаровск",
            balloonContentBody: "680032, г. Хабаровск, ул. Зеленая, д. 3а"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Хабаровск

    // Ханты-Мансийск
    var myPlacemark60 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [60.969224, 69.060188]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "628001, г. Ханты-Мансийск, пер. Рабочий, д. 3",
            balloonContentHeader: "г. Ханты-Мансийск",
            balloonContentBody: "628001, г. Ханты-Мансийск, пер. Рабочий, д. 3"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Ханты-Мансийск

    // Чебоксары
    var myPlacemark61 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [56.066300, 47.277600]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "428012, Чувашская республика, г. Чебоксары, Канашское ш., д. 7/1",
            balloonContentHeader: "г. Чебоксары",
            balloonContentBody: "428012, Чувашская республика, г. Чебоксары, Канашское ш., д. 7/1"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Чебоксары

    // Челябинск
    var myPlacemark62 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [55.229100, 61.370200]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "454008, г. Челябинск, Свердловский тракт, д. 5",
            balloonContentHeader: "г. Челябинск",
            balloonContentBody: "454008, г. Челябинск, Свердловский тракт, д. 5"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Чебоксары

    // Чита
    var myPlacemark63 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [52.063300, 113.40200]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "672003, г. Чита, ул. Трактовая, д. 55",
            balloonContentHeader: "г. Чита",
            balloonContentBody: "672003, г. Чита, ул. Трактовая, д. 55"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Чита

    // Ярославль
    var myPlacemark64 = new ymaps.GeoObject({
        geometry: {
            type: "Point",
            coordinates: [57.660800, 39.801600]
        },
        // Описываем данные геообъекта.
        properties: {
            hintContent: "150044, г. Ярославль, ул. Промышленная, д. 18д",
            balloonContentHeader: "г. Ярославль",
            balloonContentBody: "150044, г. Ярославль, ул. Промышленная, д. 18д"
        }
    }, {
        // Опции.
        // Необходимо указать данный тип макета.
        iconLayout: 'default#image',
        // Своё изображение иконки метки.
        iconImageHref: 'img/ya_map_icon.png',
        // Размеры метки.
        iconImageSize: [34, 48],
        // Хинт не вылазит за область карты.
        hintPane: 'hint'
    });
    // end Ярославль

    geoMap.geoObjects.add(myPlacemark1);
    geoMap.geoObjects.add(myPlacemark2);
    geoMap.geoObjects.add(myPlacemark3);
    geoMap.geoObjects.add(myPlacemark4);
    geoMap.geoObjects.add(myPlacemark5);
    geoMap.geoObjects.add(myPlacemark6);
    geoMap.geoObjects.add(myPlacemark7);
    geoMap.geoObjects.add(myPlacemark8);
    geoMap.geoObjects.add(myPlacemark9);
    geoMap.geoObjects.add(myPlacemark10);
    geoMap.geoObjects.add(myPlacemark11);
    geoMap.geoObjects.add(myPlacemark12);
    geoMap.geoObjects.add(myPlacemark13);
    geoMap.geoObjects.add(myPlacemark14);
    geoMap.geoObjects.add(myPlacemark15);
    geoMap.geoObjects.add(myPlacemark16);
    geoMap.geoObjects.add(myPlacemark17);
    geoMap.geoObjects.add(myPlacemark18);
    geoMap.geoObjects.add(myPlacemark19);
    geoMap.geoObjects.add(myPlacemark20);
    geoMap.geoObjects.add(myPlacemark21);
    geoMap.geoObjects.add(myPlacemark22);
    geoMap.geoObjects.add(myPlacemark23);
    geoMap.geoObjects.add(myPlacemark24);
    geoMap.geoObjects.add(myPlacemark25);
    geoMap.geoObjects.add(myPlacemark26);
    geoMap.geoObjects.add(myPlacemark27);
    geoMap.geoObjects.add(myPlacemark28);
    geoMap.geoObjects.add(myPlacemark29);
    geoMap.geoObjects.add(myPlacemark30);
    geoMap.geoObjects.add(myPlacemark31);
    geoMap.geoObjects.add(myPlacemark32);
    geoMap.geoObjects.add(myPlacemark33);
    geoMap.geoObjects.add(myPlacemark34);
    geoMap.geoObjects.add(myPlacemark35);
    geoMap.geoObjects.add(myPlacemark36);
    geoMap.geoObjects.add(myPlacemark37);
    geoMap.geoObjects.add(myPlacemark38);
    geoMap.geoObjects.add(myPlacemark39);
    geoMap.geoObjects.add(myPlacemark40);
    geoMap.geoObjects.add(myPlacemark41);
    geoMap.geoObjects.add(myPlacemark42);
    geoMap.geoObjects.add(myPlacemark43);
    geoMap.geoObjects.add(myPlacemark44);
    geoMap.geoObjects.add(myPlacemark45);
    geoMap.geoObjects.add(myPlacemark46);
    geoMap.geoObjects.add(myPlacemark47);
    geoMap.geoObjects.add(myPlacemark48);
    geoMap.geoObjects.add(myPlacemark49);
    geoMap.geoObjects.add(myPlacemark50);
    geoMap.geoObjects.add(myPlacemark51);
    geoMap.geoObjects.add(myPlacemark52);
    geoMap.geoObjects.add(myPlacemark53);
    geoMap.geoObjects.add(myPlacemark54);
    geoMap.geoObjects.add(myPlacemark55);
    geoMap.geoObjects.add(myPlacemark56);
    geoMap.geoObjects.add(myPlacemark57);
    geoMap.geoObjects.add(myPlacemark58);
    geoMap.geoObjects.add(myPlacemark59);
    geoMap.geoObjects.add(myPlacemark60);
    geoMap.geoObjects.add(myPlacemark61);
    geoMap.geoObjects.add(myPlacemark62);
    geoMap.geoObjects.add(myPlacemark63);
    geoMap.geoObjects.add(myPlacemark64);
}
// end Яндекс Карты "География поставок"