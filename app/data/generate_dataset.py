"""
Generates the comprehensive 366-day Julian fixed saints and feasts dataset
in Georgian (ka), English (en), and Russian (ru).
"""

import json
from pathlib import Path

# Base saints dictionary keyed by "MM-DD" (Julian month and day)
DATA = {
    # JANUARY (Julian: Jan 1 to Jan 31 -> Gregorian Jan 14 to Feb 13)
    "01-01": {
        "feasts": [{"code": "circumcision", "level": "great"}],
        "title_ka": "უფლისა ჩვენისა იესო ქრისტეს ხორციელი წინადაცვეთა. წმ. ბასილი დიდი",
        "title_en": "Circumcision of our Lord Jesus Christ. St. Basil the Great",
        "title_ru": "Обрезание Господне. Святителя Василия Великого",
        "saints_ka": ["ხორციელი წინადაცვეთა უფლისა ჩვენისა იესო ქრისტესი", "წმ. ბასილი დიდი, კესარია-კაპადოკიის მთავარეპისკოპოსი", "მოწამე ბასილი ანკვირიელი"],
        "saints_en": ["Circumcision of our Lord Jesus Christ", "St. Basil the Great, Archbishop of Caesarea", "Martyr Basil of Ancyra"],
        "saints_ru": ["Обрезание Господне", "Святителя Василия Великого, архиепископа Кесарии Каппадокийской", "Мученика Василия Анкирского"]
    },
    "01-02": {
        "feasts": [],
        "title_ka": "წმ. სილვესტერი, რომის პაპი. ღირსი სერაფიმე საროველი",
        "title_en": "St. Sylvester, Pope of Rome. St. Seraphim of Sarov",
        "title_ru": "Святителя Сильвестра, папы Римского. Преподобного Серафима Саровского",
        "saints_ka": ["წმ. სილვესტერი, რომის პაპი", "ღირსი სერაფიმე საროველი საკვირველთმოქმედი (მიცვალება და ნაწილთა პოვნა)", "მართალი თეოდოსი"],
        "saints_en": ["St. Sylvester, Pope of Rome", "St. Seraphim of Sarov, Wonderworker (Repose and finding of relics)", "Righteous Theodosius"],
        "saints_ru": ["Святителя Сильвестра, папы Римского", "Преподобного Серафима Саровского, чудотворца (преставление и второе обретение мощей)", "Праведного Феодосия"]
    },
    "01-03": {
        "feasts": [],
        "title_ka": "წინასწარმეტყველი მალაქია. წმ. მოწამე გორდი",
        "title_en": "Holy Prophet Malachi. Holy Martyr Gordius",
        "title_ru": "Пророка Малахии. Мученика Гордия",
        "saints_ka": ["წმ. წინასწარმეტყველი მალაქია (400 წ. ქრ.შ-მდე)", "წმ. მოწამე გორდი კესარიელი", "ღირსი პეტრე"],
        "saints_en": ["Holy Prophet Malachi (400 BC)", "Holy Martyr Gordius of Caesarea", "Venerable Peter"],
        "saints_ru": ["Пророка Малахии", "Мученика Гордия", "Преподобного Петра"]
    },
    "01-04": {
        "feasts": [],
        "title_ka": "სამოცდაათ მოციქულთა კრება",
        "title_en": "Synaxis of the Seventy Apostles",
        "title_ru": "Собор 70-ти апостолов",
        "saints_ka": ["სამოცდაათ მოციქულთა კრება (იაკობი, მარკოზი, ლუკა, კლეოპა და სხვ.)", "ღირსი თეოქტისტე"],
        "saints_en": ["Synaxis of the Seventy Apostles (James, Mark, Luke, Cleopas, etc.)", "Venerable Theoctistus"],
        "saints_ru": ["Собор 70-ти апостолов", "Преподобного Феоктиста"]
    },
    "01-05": {
        "feasts": [{"code": "theophany_eve", "level": "fast_eve"}],
        "title_ka": "ნათლისღების წინა დღე (მკაცრი მარხვა). მოწამენი თეოპემპტი და თეონა",
        "title_en": "Eve of Theophany (Strict Fast). Martyrs Theopemptus and Theonas",
        "title_ru": "Навечерие Богоявления (Крещенский сочельник). Мучеников Феопемпта и Феоны",
        "saints_ka": ["ნათლისღების წინა დღე (საქართველოსა და მსოფლიო ეკლესიებში მკაცრი მარხვა)", "წმ. მოწამენი თეოპემპტი ნიკომიდიელი ეპისკოპოსი და თეონა მოგვი", "ღირსი სინკლიტიკია ალექსანდრიელი"],
        "saints_en": ["Eve of Theophany (Paramon - Strict Fast)", "Martyrs Theopemptus, Bishop of Nicomedia, and Theonas", "Venerable Syncletica of Alexandria"],
        "saints_ru": ["Навечерие Богоявления (Крещенский сочельник)", "Священномученика Феопемпта и мученика Феоны", "Преподобной Синклитикии Александрийской"]
    },
    "01-06": {
        "feasts": [{"code": "theophany", "level": "twelve"}],
        "title_ka": "წმინდა ნათლისღება უფლისა ჩვენისა იესო ქრისტესი (ღმრთისგამოცხადება)",
        "title_en": "The Holy Theophany of our Lord and Savior Jesus Christ",
        "title_ru": "Святое Богоявление. Крещение Господа Бога и Спаса нашего Иисуса Христа",
        "saints_ka": ["ნათლისღება უფლისა ღმრთისა და მაცხოვრისა ჩვენისა იესო ქრისტესი (დიდი აიაზმა - წყალკურთხევა)"],
        "saints_en": ["The Holy Theophany and Baptism of our Lord Jesus Christ (Great Blessing of Water)"],
        "saints_ru": ["Крещение Господне (Богоявление). Великое освящение воды"]
    },
    "01-07": {
        "feasts": [{"code": "synaxis_baptist", "level": "great"}],
        "title_ka": "კრება წმინდისა და დიდებულისა წინასწარმეტყველისა, წინამორბედისა და ნათლისმცემელისა იოანესი",
        "title_en": "Synaxis of the Holy Prophet, Forerunner and Baptist John",
        "title_ru": "Собор Предтечи и Крестителя Господня Иоанна",
        "saints_ka": ["კრება წმ. იოანე ნათლისმცემლისა", "წმ. მოწამე იულიანე"],
        "saints_en": ["Synaxis of the Holy Forerunner and Baptist John", "Holy Martyr Julian"],
        "saints_ru": ["Собор Предтечи и Крестителя Господня Иоанна", "Мученика Иулиана"]
    },
    "01-08": {
        "feasts": [{"code": "st_abo_tbilisi", "level": "georgian_great"}],
        "title_ka": "წმ. მოწამე აბო თბილელი — თბილისის მფარველი. ღირსი გიორგი ქოზიბელი",
        "title_en": "Holy Martyr Abo of Tbilisi, Patron of Tbilisi. St. George the Chozebite",
        "title_ru": "Мученика Або Тбилисского. Преподобного Георгия Хозевита",
        "saints_ka": ["წმ. მოწამე აბო თბილელი (786 წ.) — თბილისის მფარველი", "ღირსი გიორგი ქოზიბელი", "ღირსი დომნიკა"],
        "saints_en": ["Holy Martyr Abo of Tbilisi (786), Heavenly Patron of Tbilisi", "Venerable George the Chozebite", "Venerable Domnica"],
        "saints_ru": ["Мученика Або Тбилисского (786)", "Преподобного Георгия Хозевита", "Преподобной Домники"]
    },
    "01-09": {
        "feasts": [],
        "title_ka": "მოწამე პოლიევქტოსი. წმ. ფილიპე, მოსკოვის მიტროპოლიტი",
        "title_en": "Martyr Polyeuctus. St. Philip, Metropolitan of Moscow",
        "title_ru": "Мученика Полиевкта. Святителя Филиппа, митрополита Московского",
        "saints_ka": ["წმ. მოწამე პოლიევქტოსი", "წმ. ფილიპე, მოსკოვისა და სრულიად რუსეთის საკვირველთმოქმედი მიტროპოლიტი"],
        "saints_en": ["Holy Martyr Polyeuctus", "St. Philip, Metropolitan of Moscow and Wonderworker"],
        "saints_ru": ["Мученика Полиевкта", "Святителя Филиппа, митрополита Московского и всея Руси, чудотворца"]
    },
    "01-10": {
        "feasts": [],
        "title_ka": "წმ. გრიგოლ ნოსელი. წმ. თეოფანე დაყუდებული",
        "title_en": "St. Gregory of Nyssa. St. Theophan the Recluse",
        "title_ru": "Святителя Григория Нисского. Святителя Феофана Затворника",
        "saints_ka": ["წმ. გრიგოლ ნოსელი ეპისკოპოსი", "წმ. თეოფანე დაყუდებული (ვიშენელი)", "ღირსი დომეთიანე მელიტინელი"],
        "saints_en": ["St. Gregory, Bishop of Nyssa", "St. Theophan the Recluse", "Venerable Dometian, Bishop of Melitene"],
        "saints_ru": ["Святителя Григория, епископа Нисского", "Святителя Феофана Затворника Вышенского", "Преподобного Дометиана Мелитинского"]
    },
    "01-11": {
        "feasts": [],
        "title_ka": "ღირსი თეოდოსი დიდი — საერთო ცხოვრების დამაარსებელი",
        "title_en": "Venerable Theodosius the Great, the Cenobiarch",
        "title_ru": "Преподобного Феодосия Великого, общих житий начальника",
        "saints_ka": ["ღირსი თეოდოსი დიდი (529 წ.)", "ღირსი მიქაელ კლოპელი"],
        "saints_en": ["Venerable Theodosius the Great (529)", "Venerable Michael of Klopsk"],
        "saints_ru": ["Преподобного Феодосия Великого (529)", "Преподобного Михаила Клопского"]
    },
    "01-12": {
        "feasts": [],
        "title_ka": "წმ. მოწამე ტატიანა. წმ. საბა სერბი",
        "title_en": "Holy Martyr Tatiana of Rome. St. Sava of Serbia",
        "title_ru": "Мученицы Татианы Римской. Святителя Саввы Сербского",
        "saints_ka": ["წმ. მოწამე ტატიანა რომაელი", "წმ. საბა I, სერბეთის მთავარეპისკოპოსი"],
        "saints_en": ["Holy Martyr Tatiana of Rome", "St. Sava I, Archbishop of Serbia"],
        "saints_ru": ["Мученицы Татианы Римской", "Святителя Саввы I, архиепископа Сербского"]
    },
    "01-13": {
        "feasts": [],
        "title_ka": "მოწამენი ერმილე და სტრატონიკე. ღირსი ირინარქე",
        "title_en": "Martyrs Hermylus and Stratonicus. Venerable Irinarchus",
        "title_ru": "Мучеников Ермила и Стратоника. Преподобного Иринарха",
        "saints_ka": ["წმ. მოწამენი ერმილე და სტრატონიკე", "ღირსი ირინარქე როსტოველი დაყუდებული"],
        "saints_en": ["Martyrs Hermylus and Stratonicus", "Venerable Irinarchus the Recluse of Rostov"],
        "saints_ru": ["Мучеников Ермила и Стратоника", "Преподобного Иринарха, затворника Ростовского"]
    },
    "01-14": {
        "feasts": [{"code": "st_nino_repose", "level": "georgian_great"}],
        "title_ka": "წმინდა მოციქულთასწორი ნინო — ქართველთა განმანათლებელი (ნინოობა). სინასა და რაითში მოწყვეტილნი მამანი",
        "title_en": "Holy Equals-to-the-Apostles Nina (Nino), Enlightener of Georgia. Holy Fathers slain at Sinai and Raithu",
        "title_ru": "Равноапостольной Нины, просветительницы Грузии. Преподобных отцев в Синае и Раифе избиенных",
        "saints_ka": ["წმ. მოციქულთასწორი ქალწული ნინო — ქართველთა განმანათლებელი (ნინოობა)", "ღირსნი მამანი, სინასა და რაითში მოწყვეტილნი (IV-V ს.)", "წმ. იოსებ ანალიტინელი"],
        "saints_en": ["Holy Equals-to-the-Apostles Nina (Nino), Enlightener of Georgia (Ninooba)", "Holy Fathers slain at Sinai and Raithu", "Venerable Joseph of Analytinus"],
        "saints_ru": ["Равноапостольной Нины, просветительницы Грузии", "Преподобных отцев, в Синае и Раифе избиенных", "Преподобного Иосифа Аналитина"]
    },
    "01-15": {
        "feasts": [],
        "title_ka": "ღირსი პავლე თებეელი და იოანე გლახაკი (კარავიტი)",
        "title_en": "Venerable Paul of Thebes and John the Hut-Dweller",
        "title_ru": "Преподобных Павла Фивейского и Иоанна Кущника",
        "saints_ka": ["ღირსი პავლე თებეელი (პირველი მეუდაბნოე)", "ღირსი იოანე კარავიტი (გლახაკი)", "ღირსი სალომე უჯარმელი და პეროჟავრა სივნიელი"],
        "saints_en": ["Venerable Paul of Thebes, First Hermit", "Venerable John the Hut-Dweller (Calabytes)", "Venerable Salome of Ujarma and Perozhavra of Sivnia"],
        "saints_ru": ["Преподобного Павла Фивейского (первого пустынника)", "Преподобного Иоанна Кущника", "Преподобных Саломии Уджармской и Перожавры Сивнийской"]
    },
    "01-16": {
        "feasts": [],
        "title_ka": "პატიოსანთა ჯაჭვთა თაყვანისცემა წმ. მოციქულისა პეტრესი",
        "title_en": "Veneration of the Precious Chains of the Holy Apostle Peter",
        "title_ru": "Поклонение честным веригам святого апостола Петра",
        "saints_ka": ["პატიოსანთა ჯაჭვთა (ბორკილთა) თაყვანისცემა წმ. მოციქულისა პეტრესი", "მოწამენი პევფილი, სპევფილი და ელევფილი"],
        "saints_en": ["Veneration of the Precious Chains of the Holy Apostle Peter", "Martyrs Speusippus, Eleusippus, and Meleusippus"],
        "saints_ru": ["Поклонение честным веригам святого апостола Петра", "Мучеников Певсиппа, Елевсиппа, Малевсиппа"]
    },
    "01-17": {
        "feasts": [{"code": "anthony_great", "level": "great"}],
        "title_ka": "ღირსი და ღმერთშემოსილი მამა ანტონი დიდი — მეუდაბნოეობის მამა",
        "title_en": "Venerable and God-bearing Father Anthony the Great",
        "title_ru": "Преподобного и богоносного отца нашего Антония Великого",
        "saints_ka": ["ღირსი ანტონი დიდი (356 წ.) — მონაზვნობის ფუძემდებელი", "წმ. ანტონი დიმსკელი"],
        "saints_en": ["Venerable Father Anthony the Great (356), Father of Monasticism", "Venerable Anthony of Dymsk"],
        "saints_ru": ["Преподобного Антония Великого (356)", "Преподобного Антония Дымского"]
    },
    "01-18": {
        "feasts": [],
        "title_ka": "წმ. ათანასე და კირილე, ალექსანდრიელი მთავარეპისკოპოსნი",
        "title_en": "Sts. Athanasius and Cyril, Archbishops of Alexandria",
        "title_ru": "Святителей Афанасия и Кирилла, архиепископов Александрийских",
        "saints_ka": ["წმ. ათანასე დიდი და კირილე ალექსანდრიელნი", "ღირსი მარკიანე კვირელი"],
        "saints_en": ["Sts. Athanasius the Great and Cyril, Archbishops of Alexandria", "Venerable Marcian of Cyrrhus"],
        "saints_ru": ["Святителей Афанасия и Кирилла, архиепископов Александрийских", "Преподобного Маркиана Кирского"]
    },
    "01-19": {
        "feasts": [],
        "title_ka": "ღირსი მაკარი დიდი ეგვიპტელი. ღირსი არსენი იყალთოელი",
        "title_en": "Venerable Macarius the Great of Egypt. St. Arsenius of Iqalto",
        "title_ru": "Преподобного Макария Великого, Египетского. Святителя Арсения Икалтойского",
        "saints_ka": ["ღირსი მაკარი დიდი ეგვიპტელი", "წმ. არსენი იყალთოელი (სწავლული ქართველი მოღვაწე)", "ღირსი მაკარი ალექსანდრიელი"],
        "saints_en": ["Venerable Macarius the Great of Egypt", "St. Arsenius of Iqalto (Georgian Scholar)", "Venerable Macarius of Alexandria"],
        "saints_ru": ["Преподобного Макария Великого, Египетского", "Святителя Арсения Икалтойского", "Преподобного Макария Александрийского"]
    },
    "01-20": {
        "feasts": [{"code": "euthymius_great", "level": "great"}],
        "title_ka": "ღირსი ევთიმი დიდი. მოწამე ინა, პინა და რიმა",
        "title_en": "Venerable Euthymius the Great. Martyrs Inna, Pinna, and Rimma",
        "title_ru": "Преподобного Евфимия Великого. Мучеников Инны, Пинны и Риммы",
        "saints_ka": ["ღირსი ევთიმი დიდი (473 წ.)", "წმ. მოწამენი ინა, პინა და რიმა"],
        "saints_en": ["Venerable Euthymius the Great (473)", "Martyrs Inna, Pinna, and Rimma"],
        "saints_ru": ["Преподобного Евфимия Великого (473)", "Мучеников Инны, Пинны и Риммы"]
    },
    "01-21": {
        "feasts": [],
        "title_ka": "ღირსი მაქსიმე აღმსარებელი. მოწამე ნეოფიტე",
        "title_en": "Venerable Maximus the Confessor. Martyr Neophytus",
        "title_ru": "Преподобного Максима Исповедника. Мученика Неофита",
        "saints_ka": ["ღირსი მაქსიმე აღმსარებელი (მისი საფლავი საქართველოში, ცაგერშია)", "წმ. მოწამე ნეოფიტე ნიკიელი", "მოწამენი ევგენი, კანდიდა, ვალერიანე და აკვილა"],
        "saints_en": ["Venerable Maximus the Confessor (his tomb is in Tsageri, Georgia)", "Holy Martyr Neophytus of Nicaea", "Martyrs Eugene, Candidus, Valerian, and Aquila"],
        "saints_ru": ["Преподобного Максима Исповедника", "Мученика Неофита Никейского", "Мучеников Евгения, Кандида, Валериана и Акилы"]
    },
    "01-22": {
        "feasts": [],
        "title_ka": "მოციქული ტიმოთე. ღირსმოწამე ანასტასი სპარსი",
        "title_en": "Apostle Timothy of the Seventy. Venerable Martyr Anastasius the Persian",
        "title_ru": "Апостола Тимофея. Преподобномученика Анастасия Персиянина",
        "saints_ka": ["წმ. მოციქული ტიმოთე (70 მოციქულთაგანი)", "ღირსმოწამე ანასტასი სპარსი"],
        "saints_en": ["Holy Apostle Timothy of the Seventy", "Venerable Martyr Anastasius the Persian"],
        "saints_ru": ["Апостола Тимофея от 70-ти", "Преподобномученика Анастасия Персиянина"]
    },
    "01-23": {
        "feasts": [],
        "title_ka": "მღვდელმოწამე კლიმენტი, ანკვირიელი ეპისკოპოსი. მოწამე აღათანგელოზი",
        "title_en": "Hieromartyr Clement, Bishop of Ancyra. Martyr Agathangelus",
        "title_ru": "Священномученика Климента, епископа Анкирского. Мученика Агафангела",
        "saints_ka": ["წმ. მღვდელმოწამე კლიმენტი ანკვირიელი და წმ. მოწამე აღათანგელოზი", "ღირსი გენადი კოსტრომელი"],
        "saints_en": ["Hieromartyr Clement, Bishop of Ancyra, and Martyr Agathangelus", "Venerable Gennadius of Kostroma"],
        "saints_ru": ["Священномученика Климента Анкирского и мученика Агафангела", "Преподобного Геннадия Костромского"]
    },
    "01-24": {
        "feasts": [],
        "title_ka": "ღირსი ქსენია (ევგენია) რომაელი. ნეტარი ქსენია პეტერბურგელი",
        "title_en": "Venerable Xenia of Rome. Blessed Xenia of St. Petersburg",
        "title_ru": "Преподобной Ксении Римляныни. Блаженной Ксении Петербургской",
        "saints_ka": ["ღირსი ქსენია (ევგენია) რომაელი", "წმ. ნეტარი ქსენია პეტერბურგელი, ქრისტესთვის სალოსი", "მოწამე ბაბილა სიცილიელი"],
        "saints_en": ["Venerable Xenia of Rome", "Blessed Xenia of St. Petersburg, Fool-for-Christ", "Martyr Babylas of Sicily"],
        "saints_ru": ["Преподобной Ксении Римляныни", "Блаженной Ксении Петербургской, Христа ради юродивой", "Мученика Вавилы Сицилийского"]
    },
    "01-25": {
        "feasts": [{"code": "gregory_theologian", "level": "great"}],
        "title_ka": "წმ. გრიგოლ ღვთისმეტყველი, კონსტანტინოპოლელი მთავარეპისკოპოსი",
        "title_en": "St. Gregory the Theologian, Archbishop of Constantinople",
        "title_ru": "Святителя Григория Богослова, архиепископа Константинопольского",
        "saints_ka": ["წმ. გრიგოლ ღვთისმეტყველი (389 წ.)", "წმ. მოწამე ფელიციტა და შვილნი მისნი", "ღირსი ანატოლი ოპტინელი"],
        "saints_en": ["St. Gregory the Theologian (389)", "Martyr Felicitas of Rome and her seven sons", "Venerable Anatoly of Optina"],
        "saints_ru": ["Святителя Григория Богослова (389)", "Мученицы Филицаты и семи сыновей ее", "Преподобного Анатолия Оптинского"]
    },
    "01-26": {
        "feasts": [{"code": "david_the_builder", "level": "georgian_great"}],
        "title_ka": "წმინდა კეთილმსახური მეფე დავით აღმაშენებელი (დავითობა). ღირსი ქსენოფონტე და მეუღლე მისი მარია",
        "title_en": "Holy Right-believing King David IV the Builder of Georgia (Davitoba). Venerable Xenophon and his wife Mary",
        "title_ru": "Благоверного царя Давида IV Возобновителя (Строителя) Грузии. Преподобного Ксенофонта и супруги его Марии",
        "saints_ka": ["წმ. კეთილმსახური მეფე დავით IV აღმაშენებელი (1125 წ.) — საქართველოს გამაერთიანებელი და უდიდესი მეფე", "ღირსი ქსენოფონტე, მეუღლე მისი მარია და შვილნი მათნი არკადი და იოანე (V-VI ს.)"],
        "saints_en": ["Holy Right-believing King David IV the Builder of Georgia (1125), Unifier of Georgia", "Venerable Xenophon, his wife Mary, and their sons Arcadius and John"],
        "saints_ru": ["Благоверного царя Давида IV Строителя (1125), объединителя Грузии", "Преподобного Ксенофонта, супруги его Марии и сыновей их Аркадия и Иоанна"]
    },
    "01-27": {
        "feasts": [{"code": "chrysostom_relics", "level": "great"}],
        "title_ka": "გადავენება პატიოსანთა ნაწილთა წმ. იოანე ოქროპირისა",
        "title_en": "Translation of the Relics of St. John Chrysostom",
        "title_ru": "Перенесение мощей святителя Иоанна Златоуста",
        "saints_ka": ["გადასვენება ნაწილთა წმ. იოანე ოქროპირისა კონსტანტინოპოლში (438 წ.)", "ღირსი მარკიანე"],
        "saints_en": ["Translation of the Relics of St. John Chrysostom to Constantinople (438)", "Venerable Marcian"],
        "saints_ru": ["Перенесение мощей святителя Иоанна Златоуста (438)", "Преподобного Маркиана"]
    },
    "01-28": {
        "feasts": [],
        "title_ka": "ღირსი ეფრემ ასური. ღირსი ისააკ ასური",
        "title_en": "Venerable Ephraim the Syrian. Venerable Isaac the Syrian",
        "title_ru": "Преподобного Ефрема Сирина. Преподобного Исаака Сирина",
        "saints_ka": ["ღირსი ეფრემ ასური (სინანულის ლოცვის ავტორი)", "ღირსი ისააკ ასური, ნინევიელი ეპისკოპოსი", "ღირსი თეოდოსი ტოტმელი"],
        "saints_en": ["Venerable Ephraim the Syrian (author of the Lenten Prayer)", "Venerable Isaac the Syrian, Bishop of Nineveh", "Venerable Theodosius of Totma"],
        "saints_ru": ["Преподобного Ефрема Сирина", "Преподобного Исаака Сирина, епископа Ниневийского", "Преподобного Феодосия Тотемского"]
    },
    "01-29": {
        "feasts": [],
        "title_ka": "გადასვენება ნაწილთა მღვდელმოწამისა იგნატი ღმერთშემოსილისა",
        "title_en": "Translation of the Relics of Hieromartyr Ignatius the God-Bearer",
        "title_ru": "Перенесение мощей священномученика Игнатия Богоносца",
        "saints_ka": ["გადასვენება ნაწილთა მღვდელმოწამისა იგნატი ღმერთშემოსილისა (107 წ.)", "წმ. მოწამენი რომანოზი, იაკობი, ფილოთეოზი და იპერექი"],
        "saints_en": ["Translation of the Relics of Hieromartyr Ignatius the God-Bearer (107)", "Martyrs Romanus, James, Philotheus, and Hyperechius"],
        "saints_ru": ["Перенесение мощей священномученика Игнатия Богоносца (107)", "Мучеников Романа, Иакова, Филофея и Иперехия"]
    },
    "01-30": {
        "feasts": [{"code": "three_hierarchs", "level": "great"}],
        "title_ka": "სამთა წმინდათა მღვდელმთავართა: ბასილი დიდისა, გრიგოლ ღვთისმეტყველისა და იოანე ოქროპირისა კრება",
        "title_en": "Synaxis of the Three Holy Hierarchs: Basil the Great, Gregory the Theologian, and John Chrysostom",
        "title_ru": "Собор вселенских учителей и святителей Василия Великого, Григория Богослова и Иоанна Златоуста",
        "saints_ka": ["სამთა უდიდესთა მსოფლიო მღვდელმთავართა და მოძღვართა კრება: ბასილი დიდი, გრიგოლ ღვთისმეტყველი და იოანე ოქროპირი", "მღვდელმოწამე იპოლიტე, რომის პაპი"],
        "saints_en": ["Synaxis of the Three Holy Hierarchs: Basil the Great, Gregory the Theologian, and John Chrysostom", "Hieromartyr Hippolytus, Pope of Rome"],
        "saints_ru": ["Собор вселенских учителей и святителей Василия Великого, Григория Богослова и Иоанна Златоуста", "Священномученика Ипполита, папы Римского"]
    },
    "01-31": {
        "feasts": [],
        "title_ka": "წმინდა უვერცხლონი კვიროსი და იოანე",
        "title_en": "Holy Unmercenaries Cyrus and John",
        "title_ru": "Святых бессребреников и чудотворцев Кира и Иоанна",
        "saints_ka": ["წმ. უვერცხლონი საკვირველთმოქმედნი კვიროსი და იოანე და მათ თანა მოწამე ათანასია და ასულნი მისნი", "წმ. ნიკიტა, ნოვგოროდელი ეპისკოპოსი"],
        "saints_en": ["Holy Unmercenaries Cyrus and John, and with them Martyr Athanasia and her daughters", "St. Nikita, Bishop of Novgorod"],
        "saints_ru": ["Святых бессребреников Кира и Иоанна и с ними мученицы Афанасии и дочерей ее", "Святителя Никиты, епископа Новгородского"]
    },

    # FEBRUARY (Julian: Feb 1 to Feb 28/29 -> Gregorian Feb 14 to Mar 13)
    "02-01": {
        "feasts": [],
        "title_ka": "მოწამე ტრიფონი",
        "title_en": "Holy Martyr Tryphon",
        "title_ru": "Мученика Трифона",
        "saints_ka": ["წმ. მოწამე ტრიფონი (250 წ.)", "მოწამენი პერპეტუა, ფელიციტა და სხვანი"],
        "saints_en": ["Holy Martyr Tryphon (250)", "Martyrs Perpetua, Felicitas, and companions"],
        "saints_ru": ["Мученика Трифона (250)", "Мучениц Перпетуи, Филицитаты и с ними"]
    },
    "02-02": {
        "feasts": [{"code": "meeting_of_the_lord", "level": "twelve"}],
        "title_ka": "მირქმა უფლისა ღმრთისა და მაცხოვრისა ჩვენისა იესო ქრისტესი",
        "title_en": "The Meeting of our Lord, God, and Savior Jesus Christ in the Temple",
        "title_ru": "Сретение Господа Бога и Спаса нашего Иисуса Христа",
        "saints_ka": ["მირქმა უფლისა ჩვენისა იესო ქრისტესი (მე-12 საუფლო დღესასწაული — მართალი სვიმეონისა და ანა წინასწარმეტყველის მიერ უფლის მიგებება ტაძარში)"],
        "saints_en": ["The Meeting of our Lord in the Temple (Presentation in the Temple - Twelve Great Feast)"],
        "saints_ru": ["Сретение Господне (Двунадесятый праздник)"]
    },
    "02-03": {
        "feasts": [],
        "title_ka": "მართალი სვიმეონ ღვთისმიმქმელი და ანა წინასწარმეტყველი",
        "title_en": "Righteous Simeon the God-Receiver and Anna the Prophetess",
        "title_ru": "Праведных Симеона Богоприимца и Анны пророчицы",
        "saints_ka": ["მართალი სვიმეონ ღვთისმიმქმელი და ანა წინასწარმეტყველი", "წმ. ნიკოლოზ იაპონელი მოციქულთასწორი"],
        "saints_en": ["Righteous Simeon the God-Receiver and Anna the Prophetess", "St. Nicholas of Japan, Equal-to-the-Apostles"],
        "saints_ru": ["Праведных Симеона Богоприимца и Анны пророчицы", "Равноапостольного Николая, архиепископа Японского"]
    },
    "02-04": {
        "feasts": [],
        "title_ka": "ღირსი ისიდორე პელუსიელი. წმ. გიორგი მთაწმინდელი (მგალობელი)",
        "title_en": "Venerable Isidore of Pelusium. St. George the Hagiorite",
        "title_ru": "Преподобного Исидора Пелусиота. Преподобного Георгия Иверского",
        "saints_ka": ["ღირსი ისიდორე პელუსიელი (436 წ.)", "წმ. კეთილმსახური მთავარი გიორგი ვსევოლოდის ძე"],
        "saints_en": ["Venerable Isidore of Pelusium (436)", "Holy Right-believing Prince George of Vladimir"],
        "saints_ru": ["Преподобного Исидора Пелусиота (436)", "Благоверного великого князя Георгия Всеволодовича"]
    },
    "02-05": {
        "feasts": [],
        "title_ka": "მოწამე აგათია (აგათა). წმ. თეოდოსი ჩერნიგოველი",
        "title_en": "Holy Martyr Agatha of Sicily. St. Theodosius, Archbishop of Chernigov",
        "title_ru": "Мученицы Агафии. Святителя Феодосия, архиепископа Черниговского",
        "saints_ka": ["წმ. მოწამე აგათია (აგათა) სიცილიელი", "წმ. თეოდოსი, ჩერნიგოველი მთავარეპისკოპოსი"],
        "saints_en": ["Holy Martyr Agatha of Sicily", "St. Theodosius, Archbishop of Chernigov"],
        "saints_ru": ["Мученицы Агафии Сицилийской", "Святителя Феодосия, архиепископа Черниговского"]
    },
    "02-06": {
        "feasts": [],
        "title_ka": "ღირსი ვუკოლა, სმირნელი ეპისკოპოსი. მოწამე დოროთეა",
        "title_en": "St. Bucolus, Bishop of Smyrna. Martyr Dorothy",
        "title_ru": "Преподобного Вукола, епископа Смирнского. Мученицы Дорофеи",
        "saints_ka": ["ღირსი ვუკოლა სმირნელი (მოციქულ იოანე ღვთისმეტყველის მოწაფე)", "წმ. მოწამე დოროთეა ქალწული და მასთან ქრისტინა, კალისტა და თეოფილი"],
        "saints_en": ["St. Bucolus, Bishop of Smyrna (disciple of St. John the Theologian)", "Martyr Dorothy the Virgin and companions"],
        "saints_ru": ["Преподобного Вукола, епископа Смирнского", "Мученицы Дорофеи девы и с нею Христины, Каллисты и Феофила"]
    },
    "02-07": {
        "feasts": [],
        "title_ka": "ღირსი პართენი ლამპსაკელი. ღირსი ლუკა ელადელი",
        "title_en": "Venerable Parthenius, Bishop of Lampsacus. Venerable Luke of Hellas",
        "title_ru": "Преподобного Парфения, епископа Лампсакийского. Преподобного Луки Елладского",
        "saints_ka": ["ღირსი პართენი, ლამპსაკიის ეპისკოპოსი", "ღირსი ლუკა ელადელი"],
        "saints_en": ["Venerable Parthenius, Bishop of Lampsacus", "Venerable Luke of Hellas"],
        "saints_ru": ["Преподобного Парфения, епископа Лампсакийского", "Преподобного Луки Елладского"]
    },
    "02-08": {
        "feasts": [],
        "title_ka": "დიდმოწამე თეოდორე სტრატილატი. წინასწარმეტყველი ზაქარია",
        "title_en": "Holy Great Martyr Theodore Stratelates. Holy Prophet Zechariah",
        "title_ru": "Великомученика Феодора Стратилата. Пророка Захарии Серповидца",
        "saints_ka": ["წმ. დიდმოწამე თეოდორე სტრატილატი (მხედართმთავარი)", "წმ. წინასწარმეტყველი ზაქარია მამხილებელი (12 მცირე წინასწარმეტყველთაგანი)"],
        "saints_en": ["Holy Great Martyr Theodore Stratelates", "Holy Prophet Zechariah the Sickle-Seeker"],
        "saints_ru": ["Великомученика Феодора Стратилата", "Пророка Захарии Серповидца"]
    },
    "02-09": {
        "feasts": [],
        "title_ka": "მოწამე ნიკიფორე ანტიოქიელი",
        "title_en": "Holy Martyr Nicephorus of Antioch",
        "title_ru": "Мученика Никифора Антиохийского",
        "saints_ka": ["წმ. მოწამე ნიკიფორე ანტიოქიელი (მიტევებისა და ძმათმოყვარეობის მაგალითი)", "მღვდელმოწამე პეტრე დამSingle"],
        "saints_en": ["Holy Martyr Nicephorus of Antioch", "Hieromartyr Peter of Damascus"],
        "saints_ru": ["Мученика Никифора, из Антиохии Сирской", "Священномученика Петра Дамаскина"]
    },
    "02-10": {
        "feasts": [],
        "title_ka": "მღვდელმოწამე ხარალამპი მაგნეზიელი",
        "title_en": "Hieromartyr Charalampus of Magnesia",
        "title_ru": "Священномученика Харалампия, епископа Магнезийского",
        "saints_ka": ["წმ. მღვდელმოწამე ხარალამპი (202 წ.) — უდიდესი მეოხი და მკურნალი", "მოწამენი პორფირი და ბაპტოსი"],
        "saints_en": ["Hieromartyr Charalampus of Magnesia (202), Wonderworker", "Martyrs Porphyrius and Baptus"],
        "saints_ru": ["Священномученика Харалампия, епископа Магнезийского (202)", "Мучеников Порфирия и Ваптоса"]
    },
    "02-11": {
        "feasts": [],
        "title_ka": "მღვდელმოწამე ვლასი სებასტიელი. მართალი თეოდორა დედოფალი",
        "title_en": "Hieromartyr Blaise, Bishop of Sebaste. Righteous Empress Theodora",
        "title_ru": "Священномученика Власия, епископа Севастийского. Праведной царицы Феодоры",
        "saints_ka": ["წმ. მღვდელმოწამე ვლასი სებასტიელი ეპისკოპოსი (316 წ.)", "წმ. მართალი დედოფალი თეოდორა, ხატთა თაყვანისცემის აღმადგენელი"],
        "saints_en": ["Hieromartyr Blaise, Bishop of Sebaste (316)", "Righteous Empress Theodora, who restored icon veneration"],
        "saints_ru": ["Священномученика Власия, епископа Севастийского (316)", "Праведной царицы Феодоры, восстановившей иконопочитание"]
    },
    "02-12": {
        "feasts": [],
        "title_ka": "წმ. მელეტი ანტიოქიელი. წმ. ალექსი, მოსკოვის მიტროპოლიტი",
        "title_en": "St. Meletius, Archbishop of Antioch. St. Alexis, Metropolitan of Moscow",
        "title_ru": "Святителя Мелетия, архиепископа Антиохийского. Святителя Алексия, митрополита Московского",
        "saints_ka": ["წმ. მელეტი ანტიოქიელი მთავარეპისკოპოსი", "წმ. ალექსი მოსკოველი საკვირველთმოქმედი"],
        "saints_en": ["St. Meletius, Archbishop of Antioch", "St. Alexis, Metropolitan of Moscow and Wonderworker"],
        "saints_ru": ["Святителя Мелетия, архиепископа Антиохийского", "Святителя Алексия, митрополита Московского, чудотворца"]
    },
    "02-13": {
        "feasts": [],
        "title_ka": "ღირსი მარტინიანე. ღირსნი ზოია და ფოტინა",
        "title_en": "Venerable Martinian of Caesarea. Venerable Zoe and Photina",
        "title_ru": "Преподобного Мартиниана. Преподобных Зои и Фотинии",
        "saints_ka": ["ღირსი მარტინიანე კესარიელი", "ღირსნი ზოია და ფოტინა (სვეტლანა)"],
        "saints_en": ["Venerable Martinian of Caesarea", "Venerable Zoe and Photina (Svetlana)"],
        "saints_ru": ["Преподобного Мартиниана Кесарийского", "Преподобных Зои и Фотинии (Светланы)"]
    },
    "02-14": {
        "feasts": [],
        "title_ka": "ღირსი ავქსენტი. მოციქულთასწორი კირილე — სლავთა განმანათლებელი",
        "title_en": "Venerable Auxentius. Holy Equal-to-the-Apostles Cyril, Teacher of the Slavs",
        "title_ru": "Преподобного Авксентия. Равноапостольного Кирилла, учителя Словенского",
        "saints_ka": ["წმ. მოციქულთასწორი კირილე ფილოსოფოსი — სლავთა განმანათლებელი", "ღირსი ავქსენტი ვითინიელი"],
        "saints_en": ["Holy Equal-to-the-Apostles Cyril, Teacher of the Slavs (869)", "Venerable Auxentius of Bithynia"],
        "saints_ru": ["Равноапостольного Кирилла, учителя Словенского (869)", "Преподобного Авксентия"]
    },
    "02-15": {
        "feasts": [],
        "title_ka": "მოციქული ონისიმე 70-თაგანი. ღირსი პაფნუტი",
        "title_en": "Apostle Onesimus of the Seventy. Venerable Paphnutius",
        "title_ru": "Апостола Онисима от 70-ти. Преподобного Пафнутия",
        "saints_ka": ["წმ. მოციქული ონისიმე (პავლე მოციქულის მოწაფე)", "ღირსი პაფნუტი განდეგილი"],
        "saints_en": ["Apostle Onesimus of the Seventy (disciple of St. Paul)", "Venerable Paphnutius the Recluse"],
        "saints_ru": ["Апостола Онисима от 70-ти", "Преподобного Пафнутия затворника"]
    },
    "02-16": {
        "feasts": [],
        "title_ka": "მოწამენი პამფილე, ვალენტი, პავლე და სხვანი",
        "title_en": "Martyrs Pamphilus, Valentus, Paul, and companions",
        "title_ru": "Мучеников Памфила, Валента, Павла и с ними",
        "saints_ka": ["წმ. მოწამე პამფილე პრესვიტერი და მასთან 11 მოწამე კესარიელი"],
        "saints_en": ["Holy Martyr Pamphilus the Presbyter and 11 companions at Caesarea"],
        "saints_ru": ["Мучеников Памфила пресвитера и с ним 11 мучеников в Кесарии"]
    },
    "02-17": {
        "feasts": [],
        "title_ka": "დიდმოწამე თეოდორე ტირონი",
        "title_en": "Holy Great Martyr Theodore the Tyro (Recruit)",
        "title_ru": "Великомученика Феодора Тирона",
        "saints_ka": ["წმ. დიდმოწამე თეოდორე ტირონი (306 წ.)", "მართალი მარიამნა"],
        "saints_en": ["Holy Great Martyr Theodore the Tyro (306)", "Righteous Mariamne, sister of Apostle Philip"],
        "saints_ru": ["Великомученика Феодора Тирона (306)", "Праведной Мариамны, сестры апостола Филиппа"]
    },
    "02-18": {
        "feasts": [],
        "title_ka": "წმ. ლეონ რომის პაპი. წმ. ფლავიანე კონსტანტინოპოლელი",
        "title_en": "St. Leo the Great, Pope of Rome. St. Flavian of Constantinople",
        "title_ru": "Святителя Льва Великого, папы Римского. Святителя Флавиана Константинопольского",
        "saints_ka": ["წმ. ლეონ I დიდი, რომის პაპი (461 წ.)", "წმ. ფლავიანე აღმსარებელი, კონსტანტინოპოლის პატრიარქი"],
        "saints_en": ["St. Leo the Great, Pope of Rome (461)", "St. Flavian the Confessor, Patriarch of Constantinople"],
        "saints_ru": ["Святителя Льва I Великого, папы Римского (461)", "Святителя Флавиана Исповедника, патриарха Константинопольского"]
    },
    "02-19": {
        "feasts": [],
        "title_ka": "მოციქულნი არქიფო და ფილიმონი 70-თაგანი",
        "title_en": "Apostles Archippus and Philemon of the Seventy",
        "title_ru": "Апостолов Архиппа и Филимона от 70-ти",
        "saints_ka": ["წმ. მოციქულნი არქიფო, ფილიმონი და მოციქულთასწორი აპფია"],
        "saints_en": ["Apostles Archippus and Philemon of the Seventy, and Apphia"],
        "saints_ru": ["Апостолов Архиппа и Филимона и мученицы Апфии"]
    },
    "02-20": {
        "feasts": [],
        "title_ka": "წმ. ლეონ კატანელი. ღირსი აგათონი",
        "title_en": "St. Leo, Bishop of Catania. Venerable Agathon",
        "title_ru": "Святителя Льва, епископа Катанского. Преподобного Агафона",
        "saints_ka": ["წმ. ლეონ კატანელი ეპისკოპოსი", "მღვდელმოწამე სადოკი სპარსი"],
        "saints_en": ["St. Leo, Bishop of Catania in Sicily", "Hieromartyr Sadoc, Bishop of Persia"],
        "saints_ru": ["Святителя Льва, епископа Катанского", "Священномученика Садока, епископа Персидского"]
    },
    "02-21": {
        "feasts": [],
        "title_ka": "ღირსი ტიმოთე სიმბოლელი. წმ. ევსტათი ანტიოქიელი",
        "title_en": "Venerable Timothy of Symbola. St. Eustathius of Antioch",
        "title_ru": "Преподобного Тимофея в Символех. Святителя Евстафия Антиохийского",
        "saints_ka": ["ღირსი ტიმოთე სიმბოლელი (მცირე აზია)", "წმ. ევსტათი ანტიოქიელი მთავარეპისკოპოსი"],
        "saints_en": ["Venerable Timothy of Symbola", "St. Eustathius, Archbishop of Antioch"],
        "saints_ru": ["Преподобного Тимофея в Символех", "Святителя Евстафия, архиепископа Антиохийского"]
    },
    "02-22": {
        "feasts": [],
        "title_ka": "პოვნა პატიოსანთა ნაწილთა წმიდათა მოწამეთა ევგენიას კარიბჭესთან",
        "title_en": "Finding of the Relics of the Holy Martyrs at Eugenius",
        "title_ru": "Обретение мощей святых мучеников во Евгении",
        "saints_ka": ["პოვნა წმიდათა მოწამეთა ნაწილთა ევგენიას კარიბჭესთან კონსტანტინოპოლში", "მოწამენი მავრიკი და 70 მხედარი"],
        "saints_en": ["Finding of the Relics of the Holy Martyrs at the Gate of Eugenius", "Martyr Maurice and 70 soldiers with him"],
        "saints_ru": ["Обретение мощей святых мучеников во Евгении", "Мученика Маврикия и 70 воинов с ним"]
    },
    "02-23": {
        "feasts": [],
        "title_ka": "მღვდელმოწამე პოლიკარპე, სმირნელი ეპისკოპოსი",
        "title_en": "Hieromartyr Polycarp, Bishop of Smyrna",
        "title_ru": "Священномученика Поликарпа, епископа Смирнского",
        "saints_ka": ["წმ. მღვდელმოწამე პოლიკარპე სმირნელი (იოანე ღვთისმეტყველის მოწაფე, 167 წ.)", "ღირსი ალექსანდრე"],
        "saints_en": ["Hieromartyr Polycarp, Bishop of Smyrna (disciple of St. John the Apostle, 167)", "Venerable Alexander"],
        "saints_ru": ["Священномученика Поликарпа, епископа Смирнского (167)", "Преподобного Александра"]
    },
    "02-24": {
        "feasts": [{"code": "first_second_finding_baptist_head", "level": "great"}],
        "title_ka": "პირველი და მეორე პოვნა პატიოსნისა თავისა წმ. იოანე ნათლისმცემლისა",
        "title_en": "First and Second Finding of the Honorable Head of St. John the Baptist",
        "title_ru": "Первое и второе обретение честной главы святого Иоанна Предтечи",
        "saints_ka": ["პირველი (IV ს.) და მეორე (452 წ.) პოვნა პატიოსნისა თავისა წმიდისა დიდებულისა წინასწარმეტყველისა და ნათლისმცემელისა იოანესი", "ღირსი ერაზმი კიევო-პეჩორელი"],
        "saints_en": ["First and Second Finding of the Precious Head of St. John the Baptist (IV c. & 452)", "Venerable Erasmus of Kiev Caves"],
        "saints_ru": ["Первое и второе обретение честной главы Иоанна Предтечи", "Преподобного Еразма Киево-Печерского"]
    },
    "02-25": {
        "feasts": [],
        "title_ka": "წმ. ტარასი, კონსტანტინოპოლელი პატრიარქი",
        "title_en": "St. Tarasius, Patriarch of Constantinople",
        "title_ru": "Святителя Тарасия, патриарха Константинопольского",
        "saints_ka": ["წმ. ტარასი კონსტანტინოპოლელი პატრიარქი (VII მსოფლიო კრების თავმჯდომარე, 806 წ.)"],
        "saints_en": ["St. Tarasius, Patriarch of Constantinople (convener of the Seventh Ecumenical Council, 806)"],
        "saints_ru": ["Святителя Тарасия, патриарха Константинопольского (806)"]
    },
    "02-26": {
        "feasts": [],
        "title_ka": "წმ. პორფირი ღაზელი ეპისკოპოსი. მოწამე სებასტიანე",
        "title_en": "St. Porphyrius, Bishop of Gaza. Martyr Sebastian",
        "title_ru": "Святителя Порфирия, архиепископа Газского. Мученика Севастиана",
        "saints_ka": ["წმ. პორფირი, ღაზის მთავარეპისკოპოსი (420 წ.)", "წმ. მოწამე სებასტიანე"],
        "saints_en": ["St. Porphyrius, Bishop of Gaza (420)", "Holy Martyr Sebastian"],
        "saints_ru": ["Святителя Порфирия, архиепископа Газского (420)", "Мученика Севастиана"]
    },
    "02-27": {
        "feasts": [],
        "title_ka": "ღირსი პროკოპი დეკაპოლელი აღმსარებელი",
        "title_en": "Venerable Procopius the Decapolite, Confessor",
        "title_ru": "Преподобного Прокопия Декаполита, исповедника",
        "saints_ka": ["ღირსი პროკოპი დეკაპოლელი აღმსარებელი (ხატმბრძოლობის წინააღმდეგ მებრძოლი)", "ღირსი ტალალე სირიელი"],
        "saints_en": ["Venerable Procopius the Decapolite, Confessor", "Venerable Thalalaeus of Syria"],
        "saints_ru": ["Преподобного Прокопия Декаполита, исповедника", "Преподобного Фалалея Сирийского"]
    },
    "02-28": {
        "feasts": [],
        "title_ka": "ღირსი ბასილი აღმსარებელი. ნეტარი ნიკოლოზ ფსკოველი",
        "title_en": "Venerable Basil the Confessor. Blessed Nicholas of Pskov",
        "title_ru": "Преподобного Василия исповедника. Блаженного Николая Псковского",
        "saints_ka": ["ღირსი ბასილი აღმსარებელი (პროკოპი დეკაპოლელის თანამოღვაწე)", "ნეტარი ნიკოლოზ სალოსი ფსკოველი", "მღვდელმოწამე პროტერი ალექსანდრიელი"],
        "saints_en": ["Venerable Basil the Confessor", "Blessed Nicholas Salos of Pskov, Fool-for-Christ", "Hieromartyr Proterius, Patriarch of Alexandria"],
        "saints_ru": ["Преподобного Василия исповедника", "Блаженного Николая Саллоса, Христа ради юродивого, Псковского", "Священномученика Протерия Александрийского"]
    },
    "02-29": {
        "feasts": [],
        "title_ka": "ღირსი იოანე კასიანე რომაელი",
        "title_en": "Venerable John Cassian the Roman",
        "title_ru": "Преподобного Иоанна Кассиана Римлянина",
        "saints_ka": ["ღირსი იოანე კასიანე რომაელი (435 წ.)", "ღირსი იოანე ვარსონოფი"],
        "saints_en": ["Venerable John Cassian the Roman (435)", "Venerable John Barsanuphius"],
        "saints_ru": ["Преподобного Иоанна Кассиана Римлянина (435)", "Преподобного Иоанна Варсонофия"]
    },
}

def generate():
    """Generates the full year canonical commemorations."""
    # Ensure remaining months are populated with rich calendar details
    import calendar_months_data
    all_data = {**DATA, **calendar_months_data.MONTHS_DATA}
    
    out_dir = Path(__file__).parent
    with open(out_dir / "saints_all.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"Generated {len(all_data)} calendar days successfully!")

if __name__ == "__main__":
    generate()
