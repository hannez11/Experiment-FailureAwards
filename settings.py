from os import environ

SESSION_CONFIGS = [
    dict(
       name='A1',
       display_name="A1",
       num_demo_participants=3,
       app_sequence=['Preexperiment'],
    ),
    dict(
       name='A2',
       display_name="A2",
       num_demo_participants=3,
       app_sequence=['Preexperiment'],
    ),
    dict(
       name='A3',
       display_name="A3",
       num_demo_participants=3,
       app_sequence=['Preexperiment'],
    ),
    dict(
       name='C0',
       display_name="C0",
       num_demo_participants=3,
       app_sequence=['Preexperiment'],
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

mturk_hit_settings = dict(
    keywords='bonus, study, experiment, research',
    title='Experimental study on decision-making (approx. 35 minutes; $4.35 compensation on average)',
    description='This HIT is a three-part study in which you 1) play a lottery 2) work on tasks concerning decision-making 3) answer a few concluding questions.',
    frame_height=500,
    template='global/mturk_template.html',
    minutes_allotted_per_assignment=120,
    expiration_hours=7 * 24,
    qualification_requirements=[
   {
        'QualificationTypeId': "00000000000000000071",
        'Comparator': "EqualTo",
        'LocaleValues': [{'Country': "US"}]
    },
    {
        'QualificationTypeId': "32Z3R27HBQLVTMC8LX4UQJ6YSR7G0I", #retake qualifaction ID
        'Comparator': "DoesNotExist",
        },
            { # Worker_​NumberHITsApproved
            'QualificationTypeId': "00000000000000000040",
            'Comparator': "GreaterThan",
            'IntegerValues': [500] #might be too high. 100 usually recommended. 500 recommended in bentley et al 2020 TAR
            },
        	{ # Worker_​NumberHITsApproved
            'QualificationTypeId': "000000000000000000L0",
            'Comparator': "GreaterThan",
            'IntegerValues': [95]
        },
    ],
    grant_qualification_id='32Z3R27HBQLVTMC8LX4UQJ6YSR7G0I', # RS account. to prevent retakes. create new qualification on mturk requester https://requester.mturk.com/qualification_types and copy paste
)

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=1.00, doc="", mturk_hit_settings=mturk_hit_settings
)

# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5pug1m_y2pz7#&0dr(s@k*#whs8=3@#cfyzj%in%n6k1woe_m-'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
