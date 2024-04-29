from myapp.models import Subject  # Import your Subject model
import sys 
reload(sys)
sys.setdefaultencoding('utf-8')
# Data for filling the Subject model
combined_array = [
    {'libar': 'الرياضيات', 'libfr': 'Mathématiques'},
    {'libar': 'القراءة', 'libfr': 'Lecture'},
    {'libar': 'الإيقاظ العلمي', 'libfr': 'Éveil scientifique'},
    {'libar': 'الخط و الإملاء', 'libfr': 'Calligraphie et orthographe'},
    {'libar': 'التربية الإسلامية', 'libfr': 'Éducation islamique'},
    {'libar': 'الإنتاج الكتابي', 'libfr': 'Production écrite'},
    {'libar': 'Lecture', 'libfr': 'Lecture'},
    {'libar': 'قواعد اللغة', 'libfr': 'Grammaire'},
    {'libar': 'Production écrite', 'libfr': 'Production écrite'},
    {'libar': 'Dictée', 'libfr': 'Dictée'},
    {'libar': 'التربية التكنولجية', 'libfr': 'Technologie éducative'},
    {'libar': 'رسم', 'libfr': 'Dessin'},
    {'libar': 'التاريخ', 'libfr': 'Histoire'},
    {'libar': 'الجغرافيا', 'libfr': 'Géographie'},
    {'libar': 'التربية المدنية', 'libfr': 'Éducation civique'},
    {'libar': 'إملاء', 'libfr': 'Orthographe'},
    {'libar': 'Anglais', 'libfr': 'Anglais'},
    {'libar': 'Langue', 'libfr': 'Langue'},
    {'libar': 'التربية المسرحية', 'libfr': 'Éducation théâtrale'},
    {'libar': 'Technologie', 'libfr': 'Technologie'},
    {'libar': 'العربية', 'libfr': 'Arabe'},
    {'libar': 'علوم الحياة والأرض', 'libfr': 'Sciences de la vie et de la terre'},
    {'libar': 'التربية الموسيقى', 'libfr': 'Éducation musicale'},
]

# Fill the Subject model with data
for item in combined_array:
    try:
        Subject.objects.get_or_create(libar=item['libar'].encode('utf-8').decode('latin-1'), libfr=item['libfr'])
    except Exception as e:
        print("Error:", e)

print("Subjects added successfully!")
