from typing import Final

DATA: Final = {
  'tyresWear': 4 * ['float'],
  'tyresDamage': 4 * ['uint8'],
  'brakesDamage': 4 * ['uint8'],
  'frontLeftWingDamage': 'uint8',
  'frontRightWingDamage': 'uint8',
  'rearWingDamage': 'uint8',
  'floorDamage': 'uint8',
  'diffuserDamage': 'uint8',
  'sidepodDamage': 'uint8',
  'drsFault': 'uint8',
  'ersFault': 'uint8',
  'gearBoxDamage': 'uint8',
  'engineDamage': 'uint8',
  'engineMGUHWear': 'uint8',
  'engineESWear': 'uint8',
  'engineCEWear': 'uint8',
  'engineICEWear': 'uint8',
  'engineMGUKWear': 'uint8',
  'engineTCWear': 'uint8',
  'engineBlown': 'uint8',
  'engineSeized': 'uint8',
}

PACKET: Final = {
  'carDamageData': 22 * [DATA]
}
