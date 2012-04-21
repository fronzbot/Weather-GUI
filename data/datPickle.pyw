import pickle
import io

USStates = ['Alabama', 'Alaska', 'American Samoa', 'Arizona', 'Arkansas',
            'California', 'Colorado', 'Connecticut', 'Delaware', 'D.C.',
            'Florida', 'Georgia', 'Guam', 'Hawaii', 'Idaho' ,'Illinois',
            'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine',
            'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
            'Missouri', 'Montana', 'Montana', 'Nebraska', 'Nevada',
            'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
            'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
            'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina',
            'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
            'Virginia', 'Virgin Islands', 'Washington', 'West Virginia',
            'Wisconsin', 'Wyoming']

CANProv = ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick',
           'Newfoundland', 'Nova Scotia', 'Nunavut', 'Ontario',
           'Prince Edward Island', 'Quebec', 'Saskatchewan', 'Yukon']

AUProv = ['Australian Capital Territory', 'Jervis Bay Territory',
          'New South Wales', 'Northern Territory', 'Queensland',
          'South Australia', 'Tasmania', 'Victoria', 'Western Australia']

AUAbbr = {'Australian Capital Territory':'ACT', 'Jervis Bay Terrirory':'JCT',
          'New South Wales':'NSW', 'Northern Territory':'NT', 'Queensland':'QLD',
          'South Australia':'SA', 'Tasmania':'TAS', 'Victoria':'VIC',
          'Western Australia':'WA'}

StateAbbr = {'Alabama':'AL','Alaska':'AK','American Samoa':'AS','Arizona':'AZ',
             'Arkansas':'AR','California':'CA','Colorado':'CO','Connecticut':'CT',
             'Delaware':'DE','D.C.':'DC','Florida':'FL','Georgia':'GA','Guam':'GU',
             'Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA',
             'Kansas':'KS','Kentucky':'KT','Louisiana':'LA','Maine':'ME','Maryland':'MD',
             'Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS',
             'Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV',
             'New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM',
             'New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH',
             'Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','Puerto Rico':'PR',
             'Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD',
             'Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA',
             'Virgin Islands':'VI','Washington':'WA','West Virginia':'WV',
             'Wisconsin':'WI','Wyoming':'WY'}

listToPickle = [USStates,
                CANProv,
                AUProv,
                AUAbbr,
                StateAbbr]

f = open('data.dat', 'wb')
pickle.dump(listToPickle, f, 3)
f.close()
