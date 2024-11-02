# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 15:21:50 2024

@author: COO1AV
"""

# Example usage:
country_request_mask = {
    'Mask': '{PartUntilCountryCode}{country_code}{PartAfterCountryCode}{request_id}',
    'PartUntilCountryCode': 'https://webtool.building-typology.eu/data/matrix/building/',
    'PartAfterCountryCode': '/p/0/o/0/l/10/dc/'
}
building_request_mask = {
    'Mask': '{PartUntilBuildingCode}{building_code}{PartAfterBuildingCode}{request_id}',
    'PartUntilBuildingCode': 'https://webtool.building-typology.eu/data/adv/building/detail/',
    'PartAfterBuildingCode': '/bv/1/dc/'
}

"Note: after bv there is the renovation phase: 1- current | 2 -scenario 1 | 3 -scenario 2"