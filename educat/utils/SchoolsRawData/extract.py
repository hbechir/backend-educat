'''
 This script is used to extract data from the excel file.
 bjeh rabi 
 note that this script should be run in a django environment
 USE: python manage.py shell
 THEN: exec(open('educat/utils/SchoolsRawData/extract.py').read())
'''


from BASE.models import Region, SchoolType, School

import pandas as pd
df = pd.read_excel('D:\\projects\\educat\\project-educat\\Backend\\educat\\educat\\utils\\SchoolsRawData\\liste_etablissement_publique.xls')


for index, row in df.iterrows():
    try:
        print(index)

        region, created = Region.objects.get_or_create(
            id=row['codedre'],
            defaults={'libar': row['libedrear']}
        )

        school_type, created = SchoolType.objects.get_or_create(
            id=row['codetypeetab'],
            defaults={'libar': row['libtypeetabar']}
        )

        school, created = School.objects.get_or_create(
            id=index,
            defaults={
                'libar': row['libeetabar'],
                'codeetab':row['codeetab'],
                'region': region,
                'school_type': school_type
            }
        )
    except Exception as e:
        print(f"Error at index {index}: {str(e)}")
