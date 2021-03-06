from rest_framework.test import APITestCase

from camphoric import models


class RegisterTests(APITestCase):
    def setUp(self):
        self.organization = models.Organization.objects.create(name="Test Organization")

    def test_dataSchema(self):
        event = models.Event.objects.create(
            organization=self.organization,
            name="Test Data Event",
            registration_schema={
                'type': 'object',
                'properties': {
                    'billing_name': {'type': 'string'},
                    'billing_address': {'type': 'string'},
                },
            },

            camper_schema={
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                },
            },
        )

        response = self.client.get(f'/api/events/{event.id}/register')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['dataSchema'], {
            'type': 'object',
            'definitions': {
                'camper': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string'},
                    },

                },
            },
            'properties': {
                'campers': {
                    'type': 'array',
                    'items': {
                        '$ref': '#/definitions/camper',
                    },
                },
                'billing_name': {'type': 'string'},
                'billing_address': {'type': 'string'},
            },
        })

    def test_uiSchema(self):
        event = models.Event.objects.create(
            organization=self.organization,
            name="Test uiSchema Event",
            registration_ui_schema={
                'ui:title': "Test UI Schema",
                'ui:description': "Test Description",
            }
        )
        response = self.client.get(f'/api/events/{event.id}/register')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['uiSchema'], {
            'ui:title': "Test UI Schema",
            'ui:description': "Test Description",
        })

    def test_pricing_fields(self):
        event = models.Event.objects.create(
            organization=self.organization,
            name="Test Price Fields",
            pricing={
                'adult': 790,
                'teen': 680,
            },
            camper_pricing_logic={
                'tuition': {'+': [1, 2]},
                'meals': {'*': [2, 3]}
            },
            registration_pricing_logic={
                'donation': {'var': 'registration.donation'}
            },
        )
        response = self.client.get(f'/api/events/{event.id}/register')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['pricing'], event.pricing)
        self.assertEqual(response.data['pricingLogic'], {
            'camper': event.camper_pricing_logic,
            'registration': event.registration_pricing_logic,
        })
