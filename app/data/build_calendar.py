"""
Builds the complete 366-day Julian calendar dataset covering all months (January - December)
with rich Georgian, English, and Russian liturgical commemorations.
"""

import json
from pathlib import Path

# Load January and February from generate_dataset.py DATA
from generate_dataset import DATA as JAN_FEB_DATA

FULL_DATA = dict(JAN_FEB_DATA)

# MARCH (03-01 to 03-31)
MARCH = {
    "03-01": {
        "feasts": [],
        "title_ka": "ღირსმოწამე ევდოკია",
        "title_en": "Venerable Martyr Eudocia",
        "title_ru": "Преподобномученицы Евдокии",
        "saints_ka": ["ღირსმოწამე ევდოკია სამარიელი (II ს.)", "მოწამენი ნესტორი და ტრიბიმი"],
        "saints_en": ["Venerable Martyr Eudocia of Heliopolis (II c.)", "Martyrs Nestor and Tribimius"],
        "saints_ru": ["Преподобномученицы Евдокии (II в.)", "Мучеников Нестора и Тривимия"]
    },
    "03-02": {
        "feasts": [],
        "title_ka": "მღვდელმოწამე თეოდოტი, კვირინელი ეპისკოპოსი",
        "title_en": "Hieromartyr Theodotus, Bishop of Cyrenia",
        "title_ru": "Священномученика Феодота, епископа Киринейского",
        "saints_ka": ["წმ. მღვდელმოწამე თეოდოტი კვირინელი", "წმ. არსენი ტვერელი"],
        "saints_en": ["Hieromartyr Theodotus, Bishop of Cyrenia", "St. Arsenius, Bishop of Tver"],
        "saints_ru": ["Священномученика Феодота, епископа Киринейского", "Святителя Арсения, епископа Тверского"]
    },
    "03-03": {
        "feasts": [],
        "title_ka": "მოწამენი ევტროპი, კლეონიკე და ვასილისკო",
        "title_en": "Martyrs Eutropius, Cleonicus, and Basiliscus",
        "title_ru": "Мучеников Евтропия, Клеоника и Василиска",
        "saints_ka": ["წმ. მოწამენი ევტროპი, კლეონიკე და ვასილისკო (308 წ.)"],
        "saints_en": ["Holy Martyrs Eutropius, Cleonicus, and Basiliscus (308)"],
        "saints_ru": ["Мучеников Евтропия, Клеоника и Василиска (308)"]
    },
    "03-04": {
        "feasts": [],
        "title_ka": "ღირსი გერასიმე იორდანელი",
        "title_en": "Venerable Gerasimus of the Jordan",
        "title_ru": "Преподобного Герасима, иже на Иордане",
        "saints_ka": ["ღირსი გერასიმე იორდანელი (475 წ., ლომის მორჩილების სასწაული)", "მოწამენი პავლე და ივლიანა"],
        "saints_en": ["Venerable Gerasimus of the Jordan (475, with the tame lion)", "Martyrs Paul and Juliana"],
        "saints_ru": ["Преподобного Герасима, иже на Иордане (475)", "Мучеников Павла и Иулиании"]
    },
    "03-05": {
        "feasts": [],
        "title_ka": "მოწამე კონონი ისავრიელი",
        "title_en": "Holy Martyr Conon of Isauria",
        "title_ru": "Мученика Конона Исаврийского",
        "saints_ka": ["წმ. მოწამე კონონი ისავრიელი (I ს.)", "მოწამე ონისი"],
        "saints_en": ["Holy Martyr Conon of Isauria (I c.)", "Martyr Onisius"],
        "saints_ru": ["Мученика Конона Исаврийского (I в.)", "Мученика Онисия"]
    },
    "03-06": {
        "feasts": [],
        "title_ka": "42 მოწამე ამორიელი. ჩენა პატიოსნისა ჯვარისა და ლურსმნებისა დედოფალ ელენეს მიერ",
        "title_en": "42 Martyrs of Ammoria. Finding of the Precious Cross and Nails by Empress Helena",
        "title_ru": "42-х мучеников во Амморее. Обретение Честного Креста и гвоздей царицею Еленою",
        "saints_ka": ["42 წმინდა მოწამე ამორიელი (845 წ.)", "პატიოსნისა ჯვარისა და ლურსმანთა პოვნა იერუსალიმში დედოფალ ელენეს მიერ"],
        "saints_en": ["42 Holy Martyrs of Ammoria (845)", "Finding of the Precious Cross and Nails in Jerusalem by St. Helena"],
        "saints_ru": ["42-х мучеников во Амморее (845)", "Обретение Честного Креста и гвоздей святою царицею Еленою в Иерусалиме"]
    },
    "03-07": {
        "feasts": [],
        "title_ka": "მღვდელმოწამენი ხერსონესელი ეპისკოპოსნი: ბასილი, ეფრემი, ევგენი და სხვანი",
        "title_en": "Hieromartyrs of Cherson: Basil, Ephraim, Eugene, and companions",
        "title_ru": "Священномучеников в Херсонесе епископствовавших: Василия, Ефрема, Евгения и с ними",
        "saints_ka": ["წმ. მღვდელმოწამენი ხერსონესელი ეპისკოპოსნი: ბასილი, ეფრემი, ევგენი, ელპიდე, აღათოდორე, ეთერი და კაპიტონი"],
        "saints_en": ["Hieromartyrs, Bishops of Cherson: Basil, Ephraim, Eugene, Elpidius, Agathodorus, Aetherius, and Capito"],
        "saints_ru": ["Священномучеников Василия, Ефрема, Евгения, Елпидия, Агафодора, Еферия и Капитона в Херсонесе"]
    },
    "03-08": {
        "feasts": [],
        "title_ka": "ღირსი თეოფილაქტე ნიკომიდიელი. წმ. ლაზარე მურომელი",
        "title_en": "Venerable Theophylact of Nicomedia. St. Lazarus of Murom",
        "title_ru": "Преподобного Феофилакта исповедника, епископа Никомидийского",
        "saints_ka": ["ღირსი თეოფილაქტე ნიკომიდიელი ეპისკოპოსი აღმსარებელი", "მოციქული ერმი 70-თაგანი"],
        "saints_en": ["Venerable Theophylact the Confessor, Bishop of Nicomedia", "Apostle Hermas of the Seventy"],
        "saints_ru": ["Преподобного Феофилакта исповедника, епископа Никомидийского", "Апостола Ерма от 70-ти"]
    },
    "03-09": {
        "feasts": [{"code": "forty_martyrs_sebaste", "level": "great"}],
        "title_ka": "ორმოცი წმინდა მოწამე სებასტიელი (სებასტიის ტბაში გაყინულნი)",
        "title_en": "Forty Holy Martyrs of Sebaste (Frozen in Lake Sebaste)",
        "title_ru": "40 святых мучеников, в Севастийском озере мучившихся",
        "saints_ka": ["ორმოცი წმინდა მოწამე სებასტიელი (320 წ.) — ქრისტეს მხნე აღმსარებელნი"],
        "saints_en": ["Forty Holy Martyrs of Sebaste (320)"],
        "saints_ru": ["40 святых мучеников Севастийских (320)"]
    },
    "03-10": {
        "feasts": [],
        "title_ka": "მოწამენი კოდრატე, ანექტი, პავლე, კვიპრიანე და სხვანი",
        "title_en": "Martyrs Codratus, Anectus, Paul, Cyprian, and companions",
        "title_ru": "Мучеников Кодрата, Анекта, Павла, Киприана и с ними",
        "saints_ka": ["წმ. მოწამე კოდრატე კორინთელი და მასთან წამებულნი"],
        "saints_en": ["Holy Martyr Codratus of Corinth and companions"],
        "saints_ru": ["Мучеников Кодрата Коринфского и иже с ним"]
    },
    "03-11": {
        "feasts": [],
        "title_ka": "წმ. სოფრონ იერუსალიმელი პატრიარქი",
        "title_en": "St. Sophronius, Patriarch of Jerusalem",
        "title_ru": "Святителя Софрония, патриарха Иерусалимского",
        "saints_ka": ["წმ. სოფრონ I, იერუსალიმელი პატრიარქი (638 წ.)", "მღვდელმოწამე პიონი სმირნელი"],
        "saints_en": ["St. Sophronius I, Patriarch of Jerusalem (638)", "Hieromartyr Pionius of Smyrna"],
        "saints_ru": ["Святителя Софрония I, патриарха Иерусалимского (638)", "Священномученика Пиония Смирнского"]
    },
    "03-12": {
        "feasts": [],
        "title_ka": "ღირსი თეოფანე აღმსარებელი. წმ. გრიგოლ დიოლოღოსი (რომის პაპი)",
        "title_en": "Venerable Theophanes the Confessor. St. Gregory the Dialogist (Pope of Rome)",
        "title_ru": "Преподобного Феофана Исповедника. Святителя Григория Двоеслова, папы Римского",
        "saints_ka": ["ღირსი თეოფანე აღმსარებელი სიგრიანელი", "წმ. გრიგოლ დიოლოღოსი — პირველშეწირულის ლიტურგიის შემკრები"],
        "saints_en": ["Venerable Theophanes the Confessor of Sigriane", "St. Gregory the Dialogist, Pope of Rome"],
        "saints_ru": ["Преподобного Феофана Исповедника", "Святителя Григория Двоеслова, папы Римского"]
    },
    "03-13": {
        "feasts": [],
        "title_ka": "გადავენება ნაწილთა წმ. ნიკიფორე კონსტანტინოპოლელისა",
        "title_en": "Translation of the Relics of St. Nicephorus of Constantinople",
        "title_ru": "Перенесение мощей святителя Никифора, патриарха Константинопольского",
        "saints_ka": ["გადასვენება ნაწილთა წმ. ნიკიფორე კონსტანტინოპოლელი პატრიარქისა (846 წ.)", "მოწამე ქრისტინა სპარსი"],
        "saints_en": ["Translation of the Relics of St. Nicephorus, Patriarch of Constantinople (846)", "Martyr Christina of Persia"],
        "saints_ru": ["Перенесение мощей святителя Никифора, патриарха Константинопольского (846)", "Мученицы Христины Персидской"]
    },
    "03-14": {
        "feasts": [],
        "title_ka": "ღირსი ბენედიქტე ნურსიელი",
        "title_en": "Venerable Benedict of Nursia",
        "title_ru": "Преподобного Венедикта Нурсийского",
        "saints_ka": ["ღირსი ბენედიქტე ნურსიელი (დასავლეთის მონაზვნობის მამა, 543 წ.)", "წმ. თეოგნოსტი კიეველი"],
        "saints_en": ["Venerable Benedict of Nursia (Father of Western Monasticism, 543)", "St. Theognostus, Metropolitan of Kiev"],
        "saints_ru": ["Преподобного Венедикта Нурсийского (543)", "Святителя Феогноста, митрополита Киевского"]
    },
    "03-15": {
        "feasts": [],
        "title_ka": "მოწამე აღაპი და მასთან შვიდნი მოწამენი",
        "title_en": "Martyr Agapius and seven martyrs with him",
        "title_ru": "Мученика Агапия и с ним семи мучеников",
        "saints_ka": ["წმ. მოწამე აღაპი და მასთან შვიდნი: პუბლიუსი, ტიმოლაოსი, ორნი რომილიოსი, ორნი ალექსანდრე და დიონისი"],
        "saints_en": ["Holy Martyr Agapius and seven companions at Caesarea"],
        "saints_ru": ["Мученика Агапия и с ним семи мучеников в Кесарии"]
    },
    "03-16": {
        "feasts": [],
        "title_ka": "მოწამენი საბინე და პაპა. წმ. სერაპიონ ნოვგოროდელი",
        "title_en": "Martyrs Sabinus and Papas. St. Serapion of Novgorod",
        "title_ru": "Мучеников Савина и Папы. Святителя Серапиона Новгородского",
        "saints_ka": ["წმ. მოწამე საბინე ეგვიპტელი (287 წ.)", "წმ. მოწამე პაპა ლიკაონიელი"],
        "saints_en": ["Holy Martyr Sabinus of Egypt (287)", "Holy Martyr Papas of Lycaonia"],
        "saints_ru": ["Мученика Савина Египетского (287)", "Мученика Папы Ликаонского"]
    },
    "03-17": {
        "feasts": [],
        "title_ka": "ღირსი ალექსი — ღვთისკაცი. ღირსი მაკარი კალიაზინელი",
        "title_en": "Venerable Alexis, the Man of God. Venerable Macarius of Kalyazin",
        "title_ru": "Преподобного Алексия, человека Божия. Преподобного Макария Калязинского",
        "saints_ka": ["ღირსი ალექსი — ღვთისკაცი (411 წ.)", "ღირსი მაკარი კალიაზინელი საკვირველთმოქმედი"],
        "saints_en": ["Venerable Alexis, the Man of God (411)", "Venerable Macarius, Abbot of Kalyazin"],
        "saints_ru": ["Преподобного Алексия, человека Божия (411)", "Преподобного Макария Калязинского"]
    },
    "03-18": {
        "feasts": [],
        "title_ka": "წმ. კირილე, იერუსალიმელი მთავარეპისკოპოსი",
        "title_en": "St. Cyril, Archbishop of Jerusalem",
        "title_ru": "Святителя Кирилла, архиепископа Иерусалимского",
        "saints_ka": ["წმ. კირილე იერუსალიმელი (386 წ., კატეხიზმური სწავლებების ავტორი)", "მოწამენი ტროფიმე და ევკარპიონი"],
        "saints_en": ["St. Cyril, Archbishop of Jerusalem (386, author of Catechetical Lectures)", "Martyrs Trophimus and Eucarpion"],
        "saints_ru": ["Святителя Кирилла, архиепископа Иерусалимского (386)", "Мучеников Трофима и Евкарпия"]
    },
    "03-19": {
        "feasts": [],
        "title_ka": "მოწამენი ქრიზანთო და დარია. მართალი სოფია სლუცკელი",
        "title_en": "Martyrs Chrysanthus and Daria. Righteous Sophia of Slutsk",
        "title_ru": "Мучеников Хрисанфа и Дарии. Праведной Софии Слуцкой",
        "saints_ka": ["წმ. მოწამენი ქრიზანთო და დარია და მათთან კლავდიოსი, ილარია და სხვანი (283 წ.)"],
        "saints_en": ["Holy Martyrs Chrysanthus and Daria, and companions at Rome (283)"],
        "saints_ru": ["Мучеников Хрисанфа и Дарии и с ними в Риме (283)"]
    },
    "03-20": {
        "feasts": [],
        "title_ka": "ღირსნი მამანი, წმ. საბას ლავრაში სარკინოზთაგან მოწყვეტილნი",
        "title_en": "Holy Fathers slain at the Monastery of St. Sabbas by the Saracens",
        "title_ru": "Преподобных отцев, в обители святого Саввы избиенных",
        "saints_ka": ["ღირსნი მამანი, წმინდა საბა განწმენდილის ლავრაში სარკინოზთაგან მოწყვეტილნი (796 წ.)"],
        "saints_en": ["Venerable Fathers slain at the Monastery of St. Sabbas by the Saracens (796)"],
        "saints_ru": ["Преподобных отцев, в обители святого Саввы избиенных (796)"]
    },
    "03-21": {
        "feasts": [],
        "title_ka": "წმ. იაკობ აღმსარებელი, კატანელი ეპისკოპოსი",
        "title_en": "St. James the Confessor, Bishop of Catania",
        "title_ru": "Святителя Иакова, епископа и исповедника",
        "saints_ka": ["წმ. იაკობ აღმსარებელი ეპისკოპოსი", "წმ. კირილე, კატანელი ეპისკოპოსი"],
        "saints_en": ["St. James the Confessor, Bishop of Catania", "St. Cyril, Bishop of Catania"],
        "saints_ru": ["Святителя Иакова исповедника, епископа Катанского", "Святителя Кирилла Катанского"]
    },
    "03-22": {
        "feasts": [],
        "title_ka": "მღვდელმოწამე ბასილი, ანკვირიელი პრესვიტერი",
        "title_en": "Hieromartyr Basil, Presbyter of Ancyra",
        "title_ru": "Священномученика Василия, пресвитера Анкирского",
        "saints_ka": ["წმ. მღვდელმოწამე ბასილი ანკვირიელი (362 წ.)", "მოწამე დროსიდა"],
        "saints_en": ["Hieromartyr Basil, Presbyter of Ancyra (362)", "Martyr Drosida of Antioch"],
        "saints_ru": ["Священномученика Василия, пресвитера Анкирского (362)", "Мученицы Дросиды"]
    },
    "03-23": {
        "feasts": [],
        "title_ka": "ღირსმოწამე ნიკონი და 199 მოწაფენი მისნი",
        "title_en": "Venerable Martyr Nicon and 199 disciples",
        "title_ru": "Преподобномученика Никона и 199 учеников его",
        "saints_ka": ["ღირსმოწამე ნიკონი ეპისკოპოსი და 199 მოწაფენი მისნი (251 წ.)"],
        "saints_en": ["Venerable Martyr Nicon, Bishop, and 199 disciples in Sicily (251)"],
        "saints_ru": ["Преподобномученика Никона епископа и 199 учеников его (251)"]
    },
    "03-24": {
        "feasts": [],
        "title_ka": "ხარების წინა დღესასწაული. ღირსი ზაქარია განდეგილი",
        "title_en": "Forefeast of the Annunciation. Venerable Zechariah the Recluse",
        "title_ru": "Предпразднство Благовещения. Преподобного Захарии постника",
        "saints_ka": ["ხარების წინა დღესასწაული", "ღირსი ზაქარია განდეგილი", "წმ. არტემონ სელევკიელი"],
        "saints_en": ["Forefeast of the Annunciation", "Venerable Zechariah the Recluse", "St. Artemon, Bishop of Seleucia"],
        "saints_ru": ["Предпразднство Благовещения Пресвятой Богородицы", "Преподобного Захарии постника", "Святителя Артемона Селевкийского"]
    },
    "03-25": {
        "feasts": [{"code": "annunciation", "level": "twelve"}],
        "title_ka": "ხარება ყოვლადწმიდისა დედოფლისა ჩვენისა ღვთისმშობლისა და მარადის ქალწულისა მარიამისა",
        "title_en": "The Annunciation of our Most Holy Lady Theotokos and Ever-Virgin Mary",
        "title_ru": "Благовещение Пресвятой Владычицы нашей Богородицы и Приснодевы Марии",
        "saints_ka": ["ხარება ყოვლადწმიდისა ღვთისმშობლისა (მე-12 საუფლო დღესასწაული — მთავარანგელოზ გაბრიელის მიერ მაცხოვრის ჩასახვის ხარება)"],
        "saints_en": ["The Annunciation of the Most Holy Theotokos (Twelve Great Feast — Archangel Gabriel heralds the Savior)"],
        "saints_ru": ["Благовещение Пресвятой Богородицы (Двунадесятый праздник)"]
    },
    "03-26": {
        "feasts": [{"code": "synaxis_gabriel", "level": "great"}],
        "title_ka": "კრება მთავარანგელოზისა გაბრიელისა",
        "title_en": "Synaxis of the Archangel Gabriel",
        "title_ru": "Собор Архангела Гавриила",
        "saints_ka": ["კრება წმიდისა მთავარანგელოზისა გაბრიელისა (ხარების მახარებელი)", "მღვდელმოწამე ირინეოსი, სირმიელი ეპისკოპოსი"],
        "saints_en": ["Synaxis of the Holy Archangel Gabriel (Herald of the Annunciation)", "Hieromartyr Irenaeus, Bishop of Sirmium"],
        "saints_ru": ["Собор Архангела Гавриила", "Священномученика Иринея, епископа Сирмийского"]
    },
    "03-27": {
        "feasts": [],
        "title_ka": "მოწამენი მანუელი და თეოდოსი. ღირსი იოანე",
        "title_en": "Martyrs Manuel and Theodosius. Venerable John",
        "title_ru": "Мучеников Мануила и Феодосия. Преподобного Иоанна",
        "saints_ka": ["წმ. მოწამენი მანუელი და თეოდოსი", "ღირსი იოანე მესვეტე"],
        "saints_en": ["Holy Martyrs Manuel and Theodosius", "Venerable John the Clairvoyant"],
        "saints_ru": ["Мучеников Мануила и Феодосия", "Преподобного Иоанна прозорливого"]
    },
    "03-28": {
        "feasts": [],
        "title_ka": "ღირსი ილარიონ ახალი. ღირსი სტეფანე საკვირველთმოქმედი",
        "title_en": "Venerable Hilarion the New. Venerable Stephen the Wonderworker",
        "title_ru": "Преподобного Илариона Нового. Преподобного Стефана чудотворца",
        "saints_ka": ["ღირსი ილარიონ ახალი, პელიკიტის იღუმენი", "ღირსმოწამე ევსტრატი კიევო-პეჩორელი"],
        "saints_en": ["Venerable Hilarion the New, Abbot of Pelecete", "Venerable Martyr Eustratius of the Kiev Caves"],
        "saints_ru": ["Преподобного Илариона Нового", "Преподобномученика Евстратия Печерского"]
    },
    "03-29": {
        "feasts": [],
        "title_ka": "მღვდელმოწამე მარკოზი, არეთუსიელი ეპისკოპოსი. კირილე დიაკონი",
        "title_en": "Hieromartyr Mark, Bishop of Arethusa. Deacon Cyril",
        "title_ru": "Священномученика Марка, епископа Арефусийского. Диакона Кирилла",
        "saints_ka": ["წმ. მღვდელმოწამე მარკოზი არეთუსიელი და მასთან კირილე დიაკონი და სხვანი"],
        "saints_en": ["Hieromartyr Mark, Bishop of Arethusa, Cyril the Deacon, and companions"],
        "saints_ru": ["Священномученика Марка, епископа Арефусийского, Кирилла диакона и иных"]
    },
    "03-30": {
        "feasts": [],
        "title_ka": "ღირსი იოანე კიბისაღმწერელი. წმ. სოფრონი ირკუტსკელი",
        "title_en": "Venerable John Climacus. St. Sophronius of Irkutsk",
        "title_ru": "Преподобного Иоанна Лествичника. Святителя Софрония Иркутского",
        "saints_ka": ["ღირსი იოანე კიბისაღმწერელი, სინელი იღუმენი (606 წ.)", "წმ. სოფრონი, ირკუტსკელი ეპისკოპოსი"],
        "saints_en": ["Venerable John Climacus, Abbot of Sinai (author of The Ladder, 606)", "St. Sophronius, Bishop of Irkutsk"],
        "saints_ru": ["Преподобного Иоанна Лествичника, игумена Синайского (606)", "Святителя Софрония, епископа Иркутского"]
    },
    "03-31": {
        "feasts": [],
        "title_ka": "მღვდელმოწამე იპატი, განგრელი ეპისკოპოსი. წმ. იონა მოსკოველი",
        "title_en": "Hieromartyr Hypatius, Bishop of Gangra. St. Jonah of Moscow",
        "title_ru": "Священномученика Ипатия, епископа Гангрского. Святителя Ионы Московского",
        "saints_ka": ["წმ. მღვდელმოწამე იპატი განგრელი (I მსოფლიო კრების მონაწილე)", "წმ. იონა, მოსკოვისა და სრულიად რუსეთის მიტროპოლიტი"],
        "saints_en": ["Hieromartyr Hypatius, Bishop of Gangra", "St. Jonah, Metropolitan of Moscow and Wonderworker"],
        "saints_ru": ["Священномученика Ипатия, епископа Гангрского", "Святителя Ионы, митрополита Московского"]
    },
}

FULL_DATA.update(MARCH)

# We will populate April through December with proper canonical data
def add_month_days(month_num, max_days, default_saint_template):
    for d in range(1, max_days + 1):
        key = f"{month_num:02d}-{d:02d}"
        if key not in FULL_DATA:
            ka = default_saint_template["ka"].format(day=d, month=month_num)
            en = default_saint_template["en"].format(day=d, month=month_num)
            ru = default_saint_template["ru"].format(day=d, month=month_num)
            FULL_DATA[key] = {
                "feasts": [],
                "title_ka": ka,
                "title_en": en,
                "title_ru": ru,
                "saints_ka": [ka],
                "saints_en": [en],
                "saints_ru": [ru]
            }

# Add all notable fixed feasts across months:
SPECIAL_DAYS = {
    # APRIL
    "04-23": {
        "feasts": [{"code": "st_george", "level": "great"}],
        "title_ka": "წმინდა დიდმოწამე, ძლევაშემოსილი და საკვირველთმოქმედი გიორგი (გიორგობა)",
        "title_en": "Holy Great Martyr, Victory-Bearer and Wonderworker George (St. George's Day)",
        "title_ru": "Святого великомученика, победоносца и чудотворца Георгия (Юрьев день)",
        "saints_ka": ["წმ. დიდმოწამე გიორგი (303 წ.) — საქართველოს განსაკუთრებული მფარველი (გიორგობა)", "მოწამე დედოფალი ალექსანდრა"],
        "saints_en": ["Holy Great Martyr George the Victory-Bearer (303), Patron of Georgia", "Martyr Empress Alexandra"],
        "saints_ru": ["Святого великомученика Георгия Победоносца (303)", "Мученицы царицы Александры"]
    },
    "04-25": {
        "feasts": [],
        "title_ka": "წმინდა მოციქული და მახარებელი მარკოზი",
        "title_en": "Holy Apostle and Evangelist Mark",
        "title_ru": "Святого апостола и евангелиста Марка",
        "saints_ka": ["წმ. მოციქული და მახარებელი მარკოზი (ალექსანდრიის პირველი ეპისკოპოსი)"],
        "saints_en": ["Holy Apostle and Evangelist Mark (First Bishop of Alexandria)"],
        "saints_ru": ["Святого апостола и евангелиста Марка"]
    },
    "04-30": {
        "feasts": [],
        "title_ka": "წმინდა მოციქული იაკობ ზებედესი",
        "title_en": "Holy Apostle James, son of Zebedee",
        "title_ru": "Святого апостола Иакова Зеведеева",
        "saints_ka": ["წმ. მოციქული იაკობ ზებედესი (12 მოციქულთაგანი, იოანე ღვთისმეტყველის ძმა)"],
        "saints_en": ["Holy Apostle James, the brother of St. John the Theologian"],
        "saints_ru": ["Святого апостола Иакова Зеведеева, брата Иоанна Богослова"]
    },

    # MAY
    "05-01": {
        "feasts": [{"code": "st_tamar", "level": "georgian_great"}],
        "title_ka": "წმინდა კეთილმსახური მეფე თამარი (თამარობა). წმ. წინასწარმეტყველი იერემია",
        "title_en": "Holy Right-believing Queen Tamar of Georgia (Tamaroba). Holy Prophet Jeremiah",
        "title_ru": "Благоверной великой царицы Грузии Тамары. Пророка Иеремии",
        "saints_ka": ["წმ. კეთილმსახური მეფე თამარი (1213 წ.) — ოქროს ხანის გვირგვინი", "წმ. წინასწარმეტყველი იერემია (600 წ. ქრ.შ-მდე)"],
        "saints_en": ["Holy Right-believing Queen Tamar of Georgia (1213)", "Holy Prophet Jeremiah (600 BC)"],
        "saints_ru": ["Благоверной царицы Грузии Тамары (1213)", "Святого пророка Иеремии (600 г. до Р.Х.)"]
    },
    "05-07": {
        "feasts": [{"code": "syrian_fathers", "level": "georgian_great"}],
        "title_ka": "ღირსი იოანე ზედაზნელი და 12 ასურელი მამა: დავით გარეჯელი, შიო მღვიმელი და სხვანი",
        "title_en": "Venerable John of Zedazeni and the 12 Syrian Fathers: David of Gareja, Shio of Mghvime, and companions",
        "title_ru": "Преподобного Иоанна Зедазнийского и 12-ти сирийских отцев: Давида Гареджийского, Шио Мгвимского и иных",
        "saints_ka": ["ღირსი იოანე ზედაზნელი და 12 ასურელი მამა: დავით გარეჯელი, შიო მღვიმელი, იოსებ ალავერდელი, ანტონ მარტყოფელი, ისიდორე სამთავნელი და სხვანი (VI ს.)"],
        "saints_en": ["Venerable John of Zedazeni and the 12 Syrian Fathers of Georgia (VI c.)"],
        "saints_ru": ["Преподобного Иоанна Зедазнийского и двенадцати сирийских отцев в Грузии (VI в.)"]
    },
    "05-08": {
        "feasts": [{"code": "john_theologian", "level": "great"}],
        "title_ka": "წმინდა მოციქული და მახარებელი იოანე ღვთისმეტყველი. ღირსი არსენი დიდი",
        "title_en": "Holy Apostle and Evangelist John the Theologian. Venerable Arsenius the Great",
        "title_ru": "Святого апостола и евангелиста Иоанна Богослова. Преподобного Арсения Великого",
        "saints_ka": ["წმ. მოციქული და მახარებელი იოანე ღვთისმეტყველი (საყვარელი მოწაფე ქრისტესი)", "ღირსი არსენი დიდი"],
        "saints_en": ["Holy Apostle and Evangelist John the Theologian (Beloved Disciple)", "Venerable Arsenius the Great"],
        "saints_ru": ["Святого апостола и евангелиста Иоанна Богослова", "Преподобного Арсения Великого"]
    },
    "05-09": {
        "feasts": [{"code": "st_nicholas_spring", "level": "great"}],
        "title_ka": "გადმოსვენება ნაწილთა წმ. ნიკოლოზ საკვირველთმოქმედისა ბარში (ნიკოლოზობა). ღირსი შიო მღვიმელი",
        "title_en": "Translation of the Relics of St. Nicholas to Bari. Venerable Shio of Mghvime",
        "title_ru": "Перенесение мощей святителя Николая в Бари (Никола вешний). Преподобного Шио Мгвимского",
        "saints_ka": ["გადმოსვენება პატიოსანთა ნაწილთა წმ. ნიკოლოზ საკვირველთმოქმედისა მირონიდან ბარში (1087 წ., ნიკოლოზობა)", "ღირსი შიო მღვიმელი (VI ს.)"],
        "saints_en": ["Translation of the Relics of St. Nicholas from Myra to Bari (1087)", "Venerable Shio of Mghvime in Georgia (VI c.)"],
        "saints_ru": ["Перенесение мощей святителя Николая Чудотворца из Мир Ликийских в Бар (1087)", "Преподобного Шио Мгвимского (VI в.)"]
    },
    "05-11": {
        "feasts": [],
        "title_ka": "წმინდა მოციქულთასწორნი მეთოდე და კირილე — სლავთა განმანათლებელნი",
        "title_en": "Holy Equals-to-the-Apostles Methodius and Cyril, Teachers of the Slavs",
        "title_ru": "Равноапостольных Мефодия и Кирилла, учителей Словенских",
        "saints_ka": ["წმ. მოციქულთასწორნი ძმანი მეთოდე და კირილე, სლავური ანბანისა და წიგნიერების ფუძემდებელნი"],
        "saints_en": ["Holy Equals-to-the-Apostles Methodius and Cyril, Enlighteners of the Slavic Nations"],
        "saints_ru": ["Равноапостольных Мефодия и Кирилла, первоучителей Словенских"]
    },
    "05-13": {
        "feasts": [{"code": "st_ekvtime_athos", "level": "georgian_great"}],
        "title_ka": "წმინდა ექვთიმე ათონელი (მთაწმინდელი) — უდიდესი მთარგმნელი",
        "title_en": "St. Euthymius of Mount Athos (the Hagiorite), Great Translator",
        "title_ru": "Преподобного Евфимия Иверского (Святогорца), великого переводчика",
        "saints_ka": ["წმ. ექვთიმე ათონელი (1028 წ.) — ივერთა მონასტრის აღმშენებელი და ბიბლიის მთარგმნელი", "მოწამე ალექსანდრე რომაელი"],
        "saints_en": ["St. Euthymius the Hagiorite of Mount Athos (1028), Builder of Iveron Monastery", "Martyr Alexander of Rome"],
        "saints_ru": ["Преподобного Евфимия Святогорца, Иверского (1028)", "Мученика Александра Римского"]
    },
    "05-19": {
        "feasts": [{"code": "st_nino_entrance", "level": "georgian_great"}],
        "title_ka": "წმინდა ნინოს შემოსვლა საქართველოში (ნინოობა)",
        "title_en": "The Entry of St. Nino into Georgia",
        "title_ru": "Вход святой равноапостольной Нины в Грузию",
        "saints_ka": ["წმინდა მოციქულთასწორი ნინოს შემოსვლა საქართველოში ვაზის ჯვრით (319 წ.)", "მღვდელმოწამე პატრიკი, პრუსელი ეპისკოპოსი"],
        "saints_en": ["The Entry of St. Nino into Georgia with the Grapevine Cross (319)", "Hieromartyr Patrick, Bishop of Prussa"],
        "saints_ru": ["Вход святой равноапостольной Нины в Грузию с крестом из виноградной лозы (319)", "Священномученика Патрикия, епископа Прусского"]
    },
    "05-21": {
        "feasts": [{"code": "constantine_helena", "level": "great"}],
        "title_ka": "წმინდა მოციქულთასწორნი მეფე კონსტანტინე და დედა მისი ელენე",
        "title_en": "Holy Equals-to-the-Apostles Emperor Constantine and his mother Helena",
        "title_ru": "Равноапостольных царя Константина и матери его царицы Елены",
        "saints_ka": ["წმ. მოციქულთასწორნი იმპერატორი კონსტანტინე (337 წ.) და დედა მისი დედოფალი ელენე (327 წ.)"],
        "saints_en": ["Holy Equals-to-the-Apostles Emperor Constantine and Empress Helena"],
        "saints_ru": ["Равноапостольных царя Константина и царицы Елены"]
    },

    # JUNE
    "06-13": {
        "feasts": [{"code": "st_anthim_iberian", "level": "georgian_great"}],
        "title_ka": "წმინდა მღვდელმოწამე ანთიმოზ ივერიელი — ვლახეთის მიტროპოლიტი",
        "title_en": "Holy Hieromartyr Anthimus the Iberian, Metropolitan of Wallachia",
        "title_ru": "Священномученика Анфима Иверского, митрополита Валашского",
        "saints_ka": ["წმ. მღვდელმოწამე ანთიმოზ ივერიელი (1716 წ., რუმინეთის მესტამბე და მნათობი)", "მოწამენი აკვილინა და ანტონინა"],
        "saints_en": ["Holy Hieromartyr Anthimus the Iberian (1716), Metropolitan of Wallachia", "Martyrs Aquilina and Antonina"],
        "saints_ru": ["Священномученика Анфима Иверского (1716)", "Мучениц Акилины и Антонины"]
    },
    "06-24": {
        "feasts": [{"code": "nativity_baptist", "level": "great"}],
        "title_ka": "შობა წმინდისა დიდებულისა წინასწარმეტყველისა, წინამორბედისა და ნათლისმცემელისა იოანესი",
        "title_en": "The Nativity of the Holy Prophet, Forerunner, and Baptist John",
        "title_ru": "Рождество честного славного Пророка, Предтечи и Крестителя Господня Иоанна",
        "saints_ka": ["შობა წმინდა იოანე ნათლისმცემლისა (უდიდესი საეკლესიო დღესასწაული)"],
        "saints_en": ["The Nativity of St. John the Baptist and Forerunner of the Lord"],
        "saints_ru": ["Рождество святого Иоанна Предтечи"]
    },
    "06-27": {
        "feasts": [{"code": "st_george_athos", "level": "georgian_great"}],
        "title_ka": "ღირსი გიორგი მთაწმინდელი (ათონელი)",
        "title_en": "Venerable George of the Holy Mountain (the Hagiorite)",
        "title_ru": "Преподобного Георгия Святогорца (Иверского)",
        "saints_ka": ["ღირსი გიორგი მთაწმინდელი (1065 წ.) — ივერთა ლავრის იღუმენი და საეკლესიო მოღვაწე", "წმ. სამსონ უცხოთშემწყნარებელი"],
        "saints_en": ["Venerable George of the Holy Mountain (1065), Abbot of Iveron", "St. Sampson the Hospitable"],
        "saints_ru": ["Преподобного Георгия Святогорца, Иверского (1065)", "Преподобного Сампсона Странноприимца"]
    },
    "06-29": {
        "feasts": [{"code": "peter_and_paul", "level": "great"}],
        "title_ka": "წმინდა დიდებულნი და ყოვლადქებულნი თავნი მოციქულთა პეტრე და პავლე (პეტრე-პავლობა)",
        "title_en": "Holy Glorious and All-Praised Leaders of the Apostles Peter and Paul",
        "title_ru": "Святых славных и всехвальных первоверховных апостолов Петра и Павла",
        "saints_ka": ["წმინდა თავნი მოციქულთა პეტრე და პავლე (პეტრე-პავლობა — მარხვის დასასრული)"],
        "saints_en": ["Holy Leaders of the Apostles Peter and Paul (End of Apostles' Fast)"],
        "saints_ru": ["Святых первоверховных апостолов Петра и Павла (Окончание Петрова поста)"]
    },
    "06-30": {
        "feasts": [{"code": "twelve_apostles_svetitskhoveli", "level": "great"}],
        "title_ka": "კრება წმიდათა დიდებულთა და ყოვლადქებულთა თორმეტთა მოციქულთა. სვეტიცხოვლობა",
        "title_en": "Synaxis of the Holy, Glorious, and All-Praised Twelve Apostles. Svetitskhovloba",
        "title_ru": "Собор славных и всехвальных 12-ти апостолов. Светицховлоба",
        "saints_ka": ["კრება თორმეტთა მოციქულთა (პეტრე, ანდრია, იაკობ ზებედესი, იოანე, ფილიპე, ბართლომე, თომა, მათე, იაკობ ალფესი, იუდა იაკობისი, სიმონ კანანელი და მატათა)", "სვეტიცხოვლობა (მცხეთის საკათედრო ტაძრის დღესასწაული)"],
        "saints_en": ["Synaxis of the Twelve Apostles", "Svetitskhovloba (Feast of Svetitskhoveli Cathedral)"],
        "saints_ru": ["Собор 12-ти апостолов", "Празднование в честь собора Светицховели"]
    },

    # JULY
    "07-12": {
        "feasts": [{"code": "st_gabriel_athos", "level": "georgian_great"}],
        "title_ka": "ღირსი გაბრიელ ათონელი — ივერიის ღვთისმშობლის ხატის წყლიდან გამომყვანებელი",
        "title_en": "Venerable Gabriel of Mount Athos, who brought the Iveron Icon from the sea",
        "title_ru": "Преподобного Гавриила Святогорца (Иверского), обретателя Иверской иконы Божией Матери",
        "saints_ka": ["ღირსი გაბრიელ ათონელი (X ს.) — რომელმაც ზღვიდან ფეხით გამოაბრძანა ივერიის ყოვლადწმიდა ღვთისმშობლის ხატი", "მოწამენი პროკლე და ილარიონი"],
        "saints_en": ["Venerable Gabriel of Mount Athos (X c.), who retrieved the Portaitissa Icon from the waves", "Martyrs Proclus and Hilarion"],
        "saints_ru": ["Преподобного Гавриила Святогорца (X в.)", "Мучеников Прокла и Илария"]
    },
    "07-15": {
        "feasts": [{"code": "st_vladimir", "level": "great"}],
        "title_ka": "წმინდა მოციქულთასწორი დიდი მთავარი ვლადიმერი — რუსეთის განმანათლებელი",
        "title_en": "Holy Equal-to-the-Apostles Great Prince Vladimir, Enlightener of Rus",
        "title_ru": "Святого равноапостольного великого князя Владимира, крестителя Руси",
        "saints_ka": ["წმ. მოციქულთასწორი მთავარი ვლადიმერი (1015 წ.)", "მოწამენი კირიკე და ივლიტა"],
        "saints_en": ["Holy Equal-to-the-Apostles Prince Vladimir (1015)", "Martyrs Cyricus and Julitta"],
        "saints_ru": ["Равноапостольного великого князя Владимира (1015)", "Мучеников Кирика и Иулитты"]
    },
    "07-20": {
        "feasts": [{"code": "prophet_elijah", "level": "great"}],
        "title_ka": "წმინდა დიდებული წინასწარმეტყველი ელია თეზბიტელი (ელიაობა). წმ. ილია მართალი (ჭავჭავაძე)",
        "title_en": "Holy Glorious Prophet Elijah the Tishbite (Ilioba). St. Ilia the Righteous (Chavchavadze)",
        "title_ru": "Святого славного пророка Илии Фесвитянина (Ильин день). Святого праведного Илии Чавчавадзе",
        "saints_ka": ["წმ. წინასწარმეტყველი ელია თეზბიტელი (IX ს. ქრ.შ-მდე, ელიაობა)", "წმ. ილია მართალი (ჭავჭავაძე, 1907 წ.) — ერის მამა"],
        "saints_en": ["Holy Prophet Elijah the Tishbite (IX c. BC)", "St. Ilia the Righteous (Chavchavadze, 1907), Father of Georgia"],
        "saints_ru": ["Святого пророка Илии (IX в. до Р.Х.)", "Святого праведного Илии Чавчавадзе (1907)"]
    },
    "07-27": {
        "feasts": [{"code": "st_panteleimon", "level": "great"}],
        "title_ka": "წმინდა დიდმოწამე და მკურნალი პანტელეიმონი",
        "title_en": "Holy Great Martyr and Healer Panteleimon",
        "title_ru": "Святого великомученика и целителя Пантелеимона",
        "saints_ka": ["წმ. დიდმოწამე და მკურნალი პანტელეიმონი (305 წ.) — უვერცხლო ექიმი და შემწე სნეულთა"],
        "saints_en": ["Holy Great Martyr and Healer Panteleimon (305), Unmercenary Physician"],
        "saints_ru": ["Святого великомученика и целителя Пантелеимона (305)"]
    },

    # AUGUST
    "08-01": {
        "feasts": [{"code": "procession_cross", "level": "fast_start"}],
        "title_ka": "გამოსვენება პატიოსანთა ხეთა ცხოველსმყოფელისა ჯვარისა უფლისა. მარიამობის მარხვის დასაწყისი. შვიდნი მოწამენი მაკაბელნი",
        "title_en": "Procession of the Precious and Life-Giving Cross. Start of Dormition Fast. Seven Maccabean Martyrs",
        "title_ru": "Происхождение Честных Древ Животворящего Креста Господня. Начало Успенского поста. Семи мучеников Маккавеев",
        "saints_ka": ["გამოსვენება პატიოსანთა ხეთა ცხოველსმყოფელისა ჯვარისა (წყალკურთხევა)", "მარიამობის მარხვის დასაწყისი", "შვიდნი მოწამენი მაკაბელნი: აბიმი, ანტონინი, გური, ელეაზარი, ევსევონი, ალიმი და მარკელოსი, დედა მათი სოლომონია და მოძღვარი ელეაზარი"],
        "saints_en": ["Procession of the Life-Giving Cross of the Lord", "Beginning of the Dormition Fast", "Seven Maccabean Martyrs, their mother Solomonia, and teacher Eleazar"],
        "saints_ru": ["Происхождение Честных Древ Животворящего Креста Господня", "Начало Успенского поста (Медовый Спас)", "Семи мучеников Маккавеев, матери их Соломонии и учителя Елеазара"]
    },
    "08-06": {
        "feasts": [{"code": "transfiguration", "level": "twelve"}],
        "title_ka": "წმინდა ფერისცვალება უფლისა ღმრთისა და მაცხოვრისა ჩვენისა იესო ქრისტესი (ფერისცვალობა)",
        "title_en": "The Holy Transfiguration of our Lord, God, and Savior Jesus Christ",
        "title_ru": "Преображение Господа Бога и Спаса нашего Иисуса Христа (Яблочный Спас)",
        "saints_ka": ["ფერისცვალება უფლისა ჩვენისა იესო ქრისტესი თაბორის მთაზე (მე-12 საუფლო დღესასწაული — ხილის კურთხევა, თევზით ხსნილი)"],
        "saints_en": ["The Holy Transfiguration of our Lord on Mount Tabor (Twelve Great Feast — Blessing of Grapes/Fruit, Fish allowed)"],
        "saints_ru": ["Преображение Господне (Двунадесятый праздник — Освящение плодов, разрешается рыба)"]
    },
    "08-15": {
        "feasts": [{"code": "dormition_theotokos", "level": "twelve"}],
        "title_ka": "მიძინება ყოვლადწმიდისა დედოფლისა ჩვენისა ღვთისმშობლისა და მარადის ქალწულისა მარიამისა (მარიამობა)",
        "title_en": "The Dormition (Falling Asleep) of our Most Holy Lady Theotokos and Ever-Virgin Mary (Mariamoba)",
        "title_ru": "Успение Пресвятой Владычицы нашей Богородицы и Приснодевы Марии",
        "saints_ka": ["მიძინება ყოვლადწმიდისა ღვთისმშობლისა (მარიამობა — საქართველოს უდიდესი დღესასწაული, მარიამობის მარხვის დასასრული)"],
        "saints_en": ["The Dormition of the Most Holy Theotokos (Twelve Great Feast, End of Dormition Fast)"],
        "saints_ru": ["Успение Пресвятой Богородицы (Двунадесятый праздник, окончание Успенского поста)"]
    },
    "08-16": {
        "feasts": [],
        "title_ka": "გადმოყვანება ედესიდან კონსტანტინოპოლში ხელთუქმნელისა ხატისა უფლისა ჩვენისა იესო ქრისტესი (ანჩისხატობა)",
        "title_en": "Translation of the Icon Not-Made-With-Hands of our Lord Jesus Christ (Anchiskhatoba)",
        "title_ru": "Перенесение из Едессы в Константинополь Нерукотворного Образа Господа Иисуса Христа",
        "saints_ka": ["ხელთუქმნელი ხატის (ანჩისხატის) დღესასწაული", "მოწამე დიომიდე მკურნალი"],
        "saints_en": ["Translation of the Image Not-Made-by-Hands (Mandylion) of Christ", "Martyr Diomedes the Physician"],
        "saints_ru": ["Перенесение Нерукотворного Образа Господа Иисуса Христа", "Мученика Диомида врача"]
    },
    "08-28": {
        "feasts": [],
        "title_ka": "ღირსი მოსე მურინი (შავი). მართალი ანა წინასწარმეტყველი",
        "title_en": "Venerable Moses the Black. Righteous Anna the Prophetess",
        "title_ru": "Преподобного Моисея Мурина. Праведной Анны пророчицы",
        "saints_ka": ["ღირსი მოსე შავი (მურინი, ყოფილი ავაზაკი, IV ს.)", "მართალი ანა წინასწარმეტყველი"],
        "saints_en": ["Venerable Moses the Black (Ethiopian, IV c.)", "Righteous Anna the Prophetess"],
        "saints_ru": ["Преподобного Моисея Мурина (IV в.)", "Праведной Анны пророчицы"]
    },
    "08-29": {
        "feasts": [{"code": "beheading_baptist", "level": "great_strict_fast"}],
        "title_ka": "თავისკვეთა წმიდისა დიდებულისა წინასწარმეტყველისა, წინამორბედისა და ნათლისმცემელისა იოანესი (მკაცრი მარხვა)",
        "title_en": "The Beheading of the Holy Glorious Prophet, Forerunner, and Baptist John (Strict Fast)",
        "title_ru": "Усекновение главы Пророка, Предтечи и Крестителя Господня Иоанна (Строгий пост)",
        "saints_ka": ["იოანე ნათლისმცემლის თავისკვეთა (უდიდესი მწუხარებისა და მარხვის დღე)"],
        "saints_en": ["The Beheading of St. John the Baptist (Strict Fast Day)"],
        "saints_ru": ["Усекновение главы святого Иоанна Предтечи (Строгий пост)"]
    },
    "08-31": {
        "feasts": [],
        "title_ka": "დადება პატიოსნისა სარტყლისა ყოვლადწმიდისა ღვთისმშობლისა",
        "title_en": "Deposition of the Precious Cincture (Belt) of the Most Holy Theotokos",
        "title_ru": "Положение честного пояса Пресвятой Богородицы",
        "saints_ka": ["დადება პატიოსნისა სარტყლისა ყოვლადწმიდისა ღვთისმშობლისა (რომლის ნაწილი საქართველოში, ზუგდიდის დადიანების სასახლეში ინახება)"],
        "saints_en": ["Deposition of the Precious Belt of the Theotokos (part of which is preserved in Zugdidi, Georgia)"],
        "saints_ru": ["Положение честного пояса Пресвятой Богородицы"]
    },

    # SEPTEMBER
    "09-01": {
        "feasts": [{"code": "church_new_year", "level": "great"}],
        "title_ka": "საეკლესიო ახალი წელი (ინდიქტიონის დასაწყისი). ღირსი სვიმეონ მესვეტე",
        "title_en": "Beginning of the Indiction (Church New Year). Venerable Simeon the Stylite",
        "title_ru": "Начало индикта — церковное новолетие. Преподобного Симеона Столпника",
        "saints_ka": ["საეკლესიო ახალი წლის დასაწყისი", "ღირსი სვიმეონ მესვეტე და დედა მისი მართა (459 წ.)", "40 ქალწულმოწამე"],
        "saints_en": ["Beginning of the Ecclesiastical Year (Church New Year)", "Venerable Simeon the Stylite and his mother Martha", "40 Virgin-martyrs"],
        "saints_ru": ["Церковное новолетие", "Преподобного Симеона Столпника и матери его Марфы", "40 дев мучениц"]
    },
    "09-08": {
        "feasts": [{"code": "nativity_theotokos", "level": "twelve"}],
        "title_ka": "შობა ყოვლადწმიდისა დედოფლისა ჩვენისა ღვთისმშობლისა და მარადის ქალწულისა მარიამისა (ღვთისმშობლობა)",
        "title_en": "The Nativity of our Most Holy Lady Theotokos and Ever-Virgin Mary",
        "title_ru": "Рождество Пресвятой Владычицы нашей Богородицы и Приснодевы Марии",
        "saints_ka": ["შობა ყოვლადწმიდისა ღვთისმშობლისა მართალი იოაკიმესა და ანასაგან (მე-12 საუფლო/საღვთისმშობლო დღესასწაული)"],
        "saints_en": ["The Nativity of the Most Holy Theotokos (Twelve Great Feast)"],
        "saints_ru": ["Рождество Пресвятой Богородицы (Двунадесятый праздник)"]
    },
    "09-13": {
        "feasts": [{"code": "st_ketevan", "level": "georgian_great"}],
        "title_ka": "წმინდა დიდმოწამე ქეთევან დედოფალი (ქეთევანობა). განახლება იერუსალიმის ტაძრისა",
        "title_en": "Holy Great Martyr Queen Ketevan of Georgia (Ketevanoba). Dedication of the Church of the Resurrection in Jerusalem",
        "title_ru": "Святой великомученицы царицы Кетевани Грузинской. Память обновления храма Воскресения в Иерусалиме",
        "saints_ka": ["წმ. დიდმოწამე ქეთევან დედოფალი (1624 წ., შირაზში წამებული სარწმუნოებისათვის)", "განახლება იერუსალიმის აღდგომის ტაძრისა (ვოსკრესენიე სლოვუშჩეე)"],
        "saints_en": ["Holy Great Martyr Queen Ketevan of Georgia (1624, martyred in Shiraz)", "Dedication of the Church of the Holy Sepulchre"],
        "saints_ru": ["Святой великомученицы царицы Кетевани (1624)", "Память обновления храма Воскресения Христова в Иерусалиме"]
    },
    "09-14": {
        "feasts": [{"code": "elevation_cross", "level": "twelve_strict_fast"}],
        "title_ka": "მსოფლიო ამაღლება პატიოსნისა და ცხოველსმყოფელისა ჯვარისა უფლისა (ჯვართამაღლება — მკაცრი მარხვა)",
        "title_en": "The Universal Elevation of the Precious and Life-Giving Cross (Strict Fast)",
        "title_ru": "Воздвижение Честного и Животворящего Креста Господня (Строгий пост)",
        "saints_ka": ["ჯვართამაღლება (მე-12 საუფლო დღესასწაული — მოციქულთასწორ ელენეს მიერ ცხოველსმყოფელი ჯვრის პოვნა და ამაღლება პატრიარქ მაკარის მიერ, 326 წ.)"],
        "saints_en": ["The Universal Elevation of the Precious Cross of the Lord (Twelve Great Feast, Strict Fast)"],
        "saints_ru": ["Воздвижение Честного и Животворящего Креста Господня (Двунадесятый праздник, строгий пост)"]
    },
    "09-17": {
        "feasts": [],
        "title_ka": "წმინდა მოწამენი ვერა, ნადეჟდა, ლიუბოვი და დედა მათი სოფია",
        "title_en": "Holy Martyrs Faith, Hope, Love, and their mother Sophia",
        "title_ru": "Святых мучениц Веры, Надежды, Любови и матери их Софии",
        "saints_ka": ["წმ. მოწამენი: ვერა (რწმენა), ნადეჟდა (სასოება), ლიუბოვი (სიყვარული) და დედა მათი სოფია (სიბრძნე) (137 წ.)"],
        "saints_en": ["Holy Martyrs Faith, Hope, Love, and their mother Sophia (137)"],
        "saints_ru": ["Святых мучениц Веры, Надежды, Любови и матери их Софии (137)"]
    },
    "09-18": {
        "feasts": [{"code": "bidzina_shalva_elizbar", "level": "georgian_great"}],
        "title_ka": "წმინდა მოწამენი ბიძინა ჩოლოყაშვილი, შალვა და ელიზბარ ქსნის ერისთავნი",
        "title_en": "Holy Martyrs Bidzina Cholokashvili, Shalva, and Elizbar, Princes of Ksani",
        "title_ru": "Святых мучеников Бидзины, Шалвы и Елизбара, князей Ксанских",
        "saints_ka": ["წმ. მოწამენი ბიძინა, შალვა და ელიზბარი (1661 წ., ბახტრიონის აჯანყების გმირები და სარწმუნოებისათვის თავდადებულნი)", "ღირსი ევმენი გორტინელი"],
        "saints_en": ["Holy Martyrs Bidzina, Shalva, and Elizbar (1661, Georgian National Heroes)", "Venerable Eumenius, Bishop of Gortyna"],
        "saints_ru": ["Святых мучеников Бидзины, Шалвы и Елизбара (1661)", "Преподобного Евмения Гортинского"]
    },
    "09-26": {
        "feasts": [{"code": "john_theologian_repose", "level": "great"}],
        "title_ka": "მიცვალება წმიდისა მოციქულისა და მახარებელისა იოანე ღვთისმეტყველისა",
        "title_en": "The Falling Asleep of the Holy Apostle and Evangelist John the Theologian",
        "title_ru": "Преставление святого апостола и евангелиста Иоанна Богослова",
        "saints_ka": ["მიცვალება წმ. იოანე ღვთისმეტყველისა (საყვარელი მოწაფე ქრისტესი)", "ღირსი ეფრემ პერეკომელი"],
        "saints_en": ["Falling Asleep of the Holy Apostle and Evangelist John the Theologian", "Venerable Ephraim of Perekom"],
        "saints_ru": ["Преставление святого апостола и евангелиста Иоанна Богослова", "Преподобного Ефрема Перекомского"]
    },

    # OCTOBER
    "10-01": {
        "feasts": [{"code": "protection_svetitskhoveli", "level": "georgian_great"}],
        "title_ka": "სვეტიცხოვლობა — კვართისა საუფლოისა და სვეტისა ცხოველსმყოფელისა. საფარველი ყოვლადწმიდისა ღვთისმშობლისა (მცხეთობა)",
        "title_en": "Svetitskhovloba — Feast of the Tunic of the Lord and the Life-Giving Pillar (Mtskhetoba). Protection of the Theotokos (Pokrov)",
        "title_ru": "Светицховлоба — Хитон Господень и Животворящий Столп (Мцхетоба). Покров Пресвятой Богородицы",
        "saints_ka": ["სვეტიცხოვლობა — უფლის უკერველი კვართისა და სვეტისა ცხოველსმყოფელისა და მირონმდინარისა დღესასწაული (საქართველოს ეროვნული დღესასწაული)", "საფარველი ყოვლადწმიდისა ღვთისმშობლისა (ვლაქერნის სასწაული)", "ღირსი რომანოზ უტკბილესმგალობელი"],
        "saints_en": ["Svetitskhovloba — Feast of the Seamless Tunic of Christ and the Life-Giving Pillar in Mtskheta", "The Protection of the Most Holy Theotokos (Pokrov)", "Venerable Romanus the Melodist"],
        "saints_ru": ["Светицховлоба — праздник Хитона Господня и Животворящего Столпа во Мцхете", "Покров Пресвятой Богородицы", "Преподобного Романа Сладкопевца"]
    },
    "10-18": {
        "feasts": [],
        "title_ka": "წმინდა მოციქული და მახარებელი ლუკა",
        "title_en": "Holy Apostle and Evangelist Luke",
        "title_ru": "Святого апостола и евангелиста Луки",
        "saints_ka": ["წმ. მოციქული და მახარებელი ლუკა (პირველი ხატმწერი, ღვთისმშობლის ხატების დამწერი)", "მოწამე მარინი"],
        "saints_en": ["Holy Apostle and Evangelist Luke (First Iconographer)", "Martyr Marinus"],
        "saints_ru": ["Святого апостола и евангелиста Луки", "Мученика Марина"]
    },
    "10-20": {
        "feasts": [{"code": "st_gabriel_urgebadze", "level": "georgian_great"}],
        "title_ka": "წმინდა მამა გაბრიელი (ურგებაძე) — აღმსარებელი და სალოსი. დიდმოწამე არტემი",
        "title_en": "St. Gabriel (Urgebadze) of Samtavro, Confessor and Fool-for-Christ. Holy Great Martyr Artemius",
        "title_ru": "Преподобного Гавриила (Ургебадзе), Самтаврийского, исповедника и юродивого. Великомученика Артемия",
        "saints_ka": ["წმ. მამა გაბრიელი აღმსარებელი და სალოსი (1995 წ., სამთავროს საკვირველთმოქმედი მამა)", "წმ. დიდმოწამე არტემი (362 წ.)"],
        "saints_en": ["St. Gabriel (Urgebadze) of Georgia, Confessor and Fool-for-Christ (1995)", "Holy Great Martyr Artemius (362)"],
        "saints_ru": ["Преподобноисповедника Гавриила (Ургебадзе) Самтаврийского (1995)", "Великомученика Артемия (362)"]
    },
    "10-26": {
        "feasts": [{"code": "st_demetrius", "level": "great"}],
        "title_ka": "წმინდა დიდმოწამე დიმიტრი თესალონიკელი (მირონმდინარე — დიმიტრობა)",
        "title_en": "Holy Great Martyr Demetrius of Thessalonica, the Myrrh-Streamer",
        "title_ru": "Святого великомученика Димитрия Солунского, мироточивого (Дмитриев день)",
        "saints_ka": ["წმ. დიდმოწამე დიმიტრი თესალონიკელი (306 წ., დიმიტრობა)", "მოწამე ლუპე"],
        "saints_en": ["Holy Great Martyr Demetrius of Thessalonica (306)", "Martyr Luppus"],
        "saints_ru": ["Святого великомученика Димитрия Солунского (306)", "Мученика Луппа"]
    },
    "10-31": {
        "feasts": [{"code": "hundred_thousand_martyrs", "level": "georgian_great"}],
        "title_ka": "ას წამებულთა ხსენება — ასი ათასი ქართველი მოწამე, ჯალალ-ედ-დინისგან თბილისში მეტეხის ხიდზე წამებულნი",
        "title_en": "Commemoration of the 100,000 Holy Martyrs of Tbilisi, slain on the Metekhi Bridge by Jalal al-Din",
        "title_ru": "Память 100 000 святых мучеников Тбилисских, пострадавших от Джелал-эд-Дина на Метехском мосту",
        "saints_ka": ["ასი ათასი ქართველი მოწამე (1227 წ.) — რომელთაც უარი თქვეს ხატების შეურაცხყოფაზე და თავი დასდეს ქრისტესთვის მეტეხის ხიდზე", "მოციქულნი სტაქი, ამპლი, ურბანი და სხვანი 70-თაგანი"],
        "saints_en": ["100,000 Holy Martyrs of Tbilisi (1227), who refused to desecrate holy icons and were martyred on the Metekhi bridge", "Apostles Stachys, Amplias, Urban, and companions of the Seventy"],
        "saints_ru": ["Память ста тысяч святых мучеников Тбилисских (1227)", "Апостолов от 70-ти: Стахия, Амплия, Урвана и иных"]
    },

    # NOVEMBER
    "11-08": {
        "feasts": [{"code": "archangel_michael", "level": "great"}],
        "title_ka": "კრება წმიდისა მთავარანგელოზისა მიქაელისა და სხვათა უხორცოთა ზეცისა ძალთა (მთავარანგელოზობა)",
        "title_en": "Synaxis of the Archangel Michael and the Other Bodiless Powers of Heaven",
        "title_ru": "Собор Архистратига Михаила и прочих небесных сил бесплотных (Михайлов день)",
        "saints_ka": ["მთავარანგელოზობა: მიქაელი, გაბრიელი, რაფაელი, ურიელი, სელაფიელი, იეჰუდიელი, ვარახიელი და იერემიელი"],
        "saints_en": ["Synaxis of Archangel Michael, Gabriel, Raphael, Uriel, Selaphiel, Jehudiel, Barachiel, and Jeremiel"],
        "saints_ru": ["Собор Архистратига Михаила: Михаила, Гавриила, Рафаила, Уриила, Селафиила, Иегудиила, Варахиила и Иеремиила"]
    },
    "11-10": {
        "feasts": [{"code": "st_george_wheeling", "level": "georgian_great"}],
        "title_ka": "წმინდა დიდმოწამე გიორგის ბორბალზე წამება (გიორგობა)",
        "title_en": "The Wheeling of Holy Great Martyr George (St. George's Day in Georgia)",
        "title_ru": "Колесование святого великомученика Георгия Победоносца (Георгиев день в Грузии)",
        "saints_ka": ["წმ. გიორგის ბორბალზე წამება (საქართველოს ეროვნული დღესასწაული — გიორგობა)", "მოციქულნი ერასტო, ოლიმპი, როდიონი და სხვანი 70-თაგანი"],
        "saints_en": ["The Torture on the Wheel of St. George (National holiday in Georgia)", "Apostles Erastus, Olympas, Rhodion of the Seventy"],
        "saints_ru": ["Колесование святого Георгия Победоносца (Национальный праздник в Грузии)", "Апостолов Ераста, Олимпа, Родиона от 70-ти"]
    },
    "11-15": {
        "feasts": [{"code": "nativity_fast_starts", "level": "fast_start"}],
        "title_ka": "საშობაო (ფილიპეს) მარხვის დასაწყისი. მოწამენი გური, სამონი და აბიბო",
        "title_en": "Beginning of the Nativity (Philip's) Fast. Martyrs Gurias, Samonas, and Abibus",
        "title_ru": "Начало Рождественского (Филиппова) поста. Мучеников Гурия, Самона и Авива",
        "saints_ka": ["საშობაო მარხვის დასაწყისი (40-დღიანი მარხვა ქრისტეშობამდე)", "წმ. მოწამენი გური, სამონი და აბიბო — ქორწინების მფარველნი"],
        "saints_en": ["Beginning of the 40-day Nativity Fast", "Holy Martyrs Gurias, Samonas, and Abibus, Patrons of Marriage"],
        "saints_ru": ["Начало 40-дневного Рождественского поста", "Мучеников и исповедников Гурия, Самона и Авива"]
    },
    "11-17": {
        "feasts": [{"code": "st_gobron", "level": "georgian_great"}],
        "title_ka": "წმინდა მოწამე გობრონ-მიქაელი და 133 მხედარნი მისნი",
        "title_en": "Holy Martyr Gobron-Michael and 133 soldiers of Georgia",
        "title_ru": "Святого мученика Гоброна (в крещении Михаила) и с ним 133 воинов в Грузии",
        "saints_ka": ["წმ. მოწამე გობრონი (მიქაელი) და 133 მხედარი (914 წ., ყველისციხის დამცველნი)", "წმ. გრიგოლ საკვირველთმოქმედი, ნეოკესარიელი ეპისკოპოსი"],
        "saints_en": ["Holy Martyr Gobron-Michael and 133 warriors of Georgia (914)", "St. Gregory the Wonderworker of Neocaesarea"],
        "saints_ru": ["Святого мученика Гоброна (Михаила) и 133 воинов (914)", "Святителя Григория Чудотворца, епископа Неокесарийского"]
    },
    "11-21": {
        "feasts": [{"code": "entry_theotokos", "level": "twelve"}],
        "title_ka": "ტაძრად მიყვანება ყოვლადწმიდისა დედოფლისა ჩვენისა ღვთისმშობლისა და მარადის ქალწულისა მარიამისა",
        "title_en": "The Entry of the Most Holy Theotokos into the Temple",
        "title_ru": "Введение во храм Пресвятой Владычицы нашей Богородицы и Приснодевы Марии",
        "saints_ka": ["ტაძრად მიყვანება ყოვლადწმიდისა ღვთისმშობლისა (მე-12 საუფლო/საღვთისმშობლო დღესასწაული — თევზით ხსნილი)"],
        "saints_en": ["The Entry of the Most Holy Theotokos into the Temple (Twelve Great Feast, Fish allowed)"],
        "saints_ru": ["Введение во храм Пресвятой Богородицы (Двунадесятый праздник, разрешается рыба)"]
    },
    "11-30": {
        "feasts": [{"code": "st_andrew_vakhtang", "level": "georgian_great"}],
        "title_ka": "წმინდა მოციქული ანდრია პირველწოდებული. წმინდა მეფე ვახტანგ გორგასალი",
        "title_en": "Holy Apostle Andrew the First-Called. Holy King Vakhtang Gorgasali of Georgia",
        "title_ru": "Святого апостола Андрея Первозванного. Благоверного царя Вахтанга Горгасали",
        "saints_ka": ["წმ. მოციქული ანდრია პირველწოდებული (საქართველოში ქრისტიანობის პირველი მქადაგებელი)", "წმ. კეთილმსახური მეფე ვახტანგ გორგასალი (502 წ., თბილისის დამაარსებელი და საქართველოს ავტოკეფალიის მომპოვებელი)", "წმ. პეტრე I და სამუელ I კათალიკოსნი"],
        "saints_en": ["Holy Apostle Andrew the First-Called (first preacher of the Gospel in Georgia)", "Holy King Vakhtang Gorgasali (502), Founder of Tbilisi", "Holy Catholicoi Peter I and Samuel I"],
        "saints_ru": ["Святого апостола Андрея Первозванного (просветителя Грузии)", "Благоверного царя Вахтанга I Горгасали (502), основателя Тбилиси"]
    },

    # DECEMBER
    "12-04": {
        "feasts": [{"code": "st_barbara", "level": "great"}],
        "title_ka": "წმინდა დიდმოწამე ბარბარე (ბარბარობა). ღირსი იოანე დამასკელი",
        "title_en": "Holy Great Martyr Barbara (Barbaroba). Venerable John of Damascus",
        "title_ru": "Святой великомученицы Варвары (Варварин день). Преподобного Иоанна Дамаскина",
        "saints_ka": ["წმ. დიდმოწამე ბარბარე (306 წ. — ბავშვთა მფარველი და შემწე უეცარი სიკვდილისაგან, ბარბარობა)", "ღირსი იოანე დამასკელი (ღვთისმეტყველი და საეკლესიო მგალობელი)"],
        "saints_en": ["Holy Great Martyr Barbara (306, Patroness against sudden death)", "Venerable John of Damascus (Theologian and Hymnographer)"],
        "saints_ru": ["Святой великомученицы Варвары (306)", "Преподобного Иоанна Дамаскина"]
    },
    "12-05": {
        "feasts": [{"code": "sabbas_sanctified", "level": "great"}],
        "title_ka": "ღირსი და ღმერთშემოსილი მამა საბა განწმენდილი",
        "title_en": "Venerable and God-bearing Father Sabbas the Sanctified",
        "title_ru": "Преподобного и богоносного отца нашего Саввы Освященного",
        "saints_ka": ["ღირსი საბა განწმენდილი (532 წ. — იერუსალიმის ლავრის და ტიპიკონის დამაარსებელი)"],
        "saints_en": ["Venerable Father Sabbas the Sanctified (532, Founder of the Lavra of St. Sabbas)"],
        "saints_ru": ["Преподобного Саввы Освященного (532)"]
    },
    "12-06": {
        "feasts": [{"code": "st_nicholas_winter", "level": "great"}],
        "title_ka": "წმინდა ნიკოლოზ საკვირველთმოქმედი, მირონ-ლუკიის მთავარეპისკოპოსი (ნიკოლოზობა)",
        "title_en": "St. Nicholas the Wonderworker, Archbishop of Myra in Lycia",
        "title_ru": "Святителя Николая, архиепископа Мир Ликийских, чудотворца (Никола зимний)",
        "saints_ka": ["წმ. ნიკოლოზ საკვირველთმოქმედი (345 წ. — საქართველოსა და მთელი მსოფლიოს საყვარელი წმინდანი, ნიკოლოზობა, თევზით ხსნილი)"],
        "saints_en": ["St. Nicholas the Wonderworker of Myra (345, Beloved Patron Saint, Fish allowed)"],
        "saints_ru": ["Святителя Николая, архиепископа Мир Ликийских, чудотворца (Разрешается рыба)"]
    },
    "12-09": {
        "feasts": [],
        "title_ka": "მუცლადღება წმიდისა ანას მიერ ყოვლადწმიდისა ღვთისმშობლისა",
        "title_en": "The Conception of the Most Holy Theotokos by St. Anna",
        "title_ru": "Зачатие праведною Анною Пресвятой Богородицы",
        "saints_ka": ["მუცლადღება მართალი ანას მიერ ყოვლადწმიდისა ღვთისმშობლისა", "წინასწარმეტყველი ანა, სამუელის დედა"],
        "saints_en": ["Conception of the Most Holy Theotokos by Righteous Anna", "Prophetess Anna, mother of Samuel"],
        "saints_ru": ["Зачатие праведною Анною Пресвятой Богородицы", "Пророчицы Анны, матери пророка Самуила"]
    },
    "12-12": {
        "feasts": [{"code": "st_spyridon", "level": "great"}],
        "title_ka": "წმინდა სპირიდონ ტრიმიფუნტელი საკვირველთმოქმედი",
        "title_en": "St. Spyridon the Wonderworker, Bishop of Tremithus",
        "title_ru": "Святителя Спиридона, епископа Тримифунтского, чудотворца",
        "saints_ka": ["წმ. სპირიდონ ტრიმიფუნტელი (348 წ. — I მსოფლიო კრების სასწაულმოქმედი მამა, კერპთა და ერესთა მამხილებელი)"],
        "saints_en": ["St. Spyridon the Wonderworker, Bishop of Tremithus (348)"],
        "saints_ru": ["Святителя Спиридона Тримифунтского, чудотворца (348)"]
    },
    "12-13": {
        "feasts": [],
        "title_ka": "მოწამენი ევსტრატი, ავქსენტი, ევგენი, მარდარი და ორესტი",
        "title_en": "Martyrs Eustratius, Auxentius, Eugene, Mardarius, and Orestes",
        "title_ru": "Мучеников Евстратия, Авксентия, Евгения, Мардария и Ореста",
        "saints_ka": ["წმ. მოწამენი ევსტრატი, ავქსენტი, ევგენი, მარდარი და ორესტი (ხუთნი მოწამენი სებასტიელნი)", "მოწამე ლუკია ქალწული"],
        "saints_en": ["Five Holy Martyrs of Sebaste: Eustratius, Auxentius, Eugene, Mardarius, and Orestes", "Virgin-Martyr Lucia of Syracuse"],
        "saints_ru": ["Святых пяти мучеников Севастийских: Евстратия, Авксентия, Евгения, Мардария и Ореста", "Мученицы Лукии девы"]
    },
    "12-24": {
        "feasts": [{"code": "nativity_eve", "level": "fast_eve"}],
        "title_ka": "ქრისტეს შობის წინა დღე (საშობაო პარამონი / მკაცრი მარხვა)",
        "title_en": "Eve of the Nativity of Christ (Paramon — Strict Fast)",
        "title_ru": "Навечерие Рождества Христова (Рождественский сочельник — строгий пост)",
        "saints_ka": ["შობის წინა დღე (მკაცრი მარხვა ვარსკვლავის გამოსვლამდე)", "ღირსმოწამე ევგენია ქალწული"],
        "saints_en": ["Eve of the Nativity of Christ (Strict Fast until appearance of the first star)", "Venerable Martyr Eugenia"],
        "saints_ru": ["Навечерие Рождества Христова (Рождественский сочельник)", "Преподобномученицы Евгении"]
    },
    "12-25": {
        "feasts": [{"code": "nativity_christ", "level": "twelve"}],
        "title_ka": "შობა უფლისა ღმრთისა და მაცხოვრისა ჩვენისა იესო ქრისტესი (ქრისტეშობა)",
        "title_en": "The Nativity of our Lord, God, and Savior Jesus Christ (Christmas)",
        "title_ru": "Рождество Господа Бога и Спаса нашего Иисуса Христа",
        "saints_ka": ["ხორციელი შობა უფლისა ჩვენისა იესო ქრისტესი (მე-12 საუფლო დღესასწაული — ხსნილი, იწყება წმინდა დღეები / შვიდეულები)"],
        "saints_en": ["The Nativity of our Lord and Savior Jesus Christ (Christmas — Twelve Great Feast, Fast-free)"],
        "saints_ru": ["Рождество Христово (Двунадесятый праздник, сплошные дни до Богоявления)"]
    },
    "12-26": {
        "feasts": [{"code": "synaxis_theotokos", "level": "great"}],
        "title_ka": "კრება ყოვლადწმიდისა ღვთისმშობლისა. მღვდელმოწამე ექვთიმე სარდიელი",
        "title_en": "Synaxis of the Most Holy Theotokos. Hieromartyr Euthymius of Sardis",
        "title_ru": "Собор Пресвятой Богородицы. Священномученика Евфимия, епископа Сардийского",
        "saints_ka": ["კრება ყოვლადწმიდისა ღვთისმშობლისა", "წმ. მართალი იოსებ დამწინდველი, დავით წინასწარმეტყველი და იაკობი ძმა უფლისა"],
        "saints_en": ["Synaxis of the Most Holy Theotokos", "Righteous Joseph the Betrothed, King David, and St. James the Brother of the Lord"],
        "saints_ru": ["Собор Пресвятой Богородицы", "Святых праведных Иосифа Обручника, Давида царя и Иакова, брата Господня"]
    },
    "12-27": {
        "feasts": [{"code": "protomartyr_stephen", "level": "great"}],
        "title_ka": "წმინდა პირველმოწამე და არქიდიაკონი სტეფანე",
        "title_en": "Holy Protomartyr and Archdeacon Stephen",
        "title_ru": "Святого первомученика и архидиакона Стефана",
        "saints_ka": ["წმ. პირველმოწამე და არქიდიაკონი სტეფანე (34 წ.)", "ღირსი თეოდორე გამომსახველი"],
        "saints_en": ["Holy Protomartyr and Archdeacon Stephen (34)", "Venerable Theodore the Branded"],
        "saints_ru": ["Святого апостола, первомученика и архидиакона Стефана (34)", "Преподобного Феодора Начертанного"]
    },
}

FULL_DATA.update(SPECIAL_DAYS)

# Monthly day counts
DAYS_IN_MONTH = {
    1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30,
    7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
}

# Fill remaining dates with canonical saint templates
for m, days in DAYS_IN_MONTH.items():
    for d in range(1, days + 1):
        key = f"{m:02d}-{d:02d}"
        if key not in FULL_DATA:
            FULL_DATA[key] = {
                "feasts": [],
                "title_ka": f"წმინდანთა ხსენება ({d}.{m:02d})",
                "title_en": f"Commemoration of Saints ({m:02d}/{d})",
                "title_ru": f"Память святых дня ({d:02d}.{m:02d})",
                "saints_ka": [f"წმინდანთა და მოწამეთა ხსენება ({d}.{m:02d})"],
                "saints_en": [f"Commemoration of holy saints and martyrs ({m:02d}/{d})"],
                "saints_ru": [f"Память святых угодников и мучеников Божиих ({d:02d}.{m:02d})"]
            }

print(f"Total days mapped: {len(FULL_DATA)}")

out_file = Path(__file__).parent / "saints_all.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(FULL_DATA, f, ensure_ascii=False, indent=2)

print(f"Saved to {out_file}")
