from numpy import nan
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

df = pd.read_csv("https://data.cityofnewyork.us/resource/vfnx-vebw.csv")
"""
Northwest corner: 40.8011° N, 73.9654° W
Northeast corner: 40.7972° N, 73.9497° W
Southwest corner: 40.7648° N, 73.9742° W
Southeast corner: 40.7641° N, 73.9583° W
"""
y_mid = (40.8011 + 40.7641 + 40.7972 + 40.7648)/4
x_mid = -(73.9742 + 73.9497 + 73.9654 + 73.9583)/4

###  run on columns to extrat the output dataset columns

## start an empty dataframe with column name:
# print(df['primary_fur_color'].unique())
# print(df['highlight_fur_color'].unique())
output_columns = ['Upperwest', 'Uppereast', 'Lowerwest', 'Lowereast', 'AM', 'PM', 'Adult', 'Juvenile', 'Unkown_Age',
                  'Main_Gray', 'Main_Cinnamon', 'Main_Black', 'Main_Other_Color',
                  'HL_Cinnamon', 'HL_White', 'HL_Gray', 'HL_Cinnamon_White', 'HL_Gray_White', 'HL_Black_Cinnamon_White', 'HL_Black', 'HL_Black_White', 'HL_Black_Cinnamon', 'HL_Other',
                  'Above_Ground', 'Grond_Plane', "Ground_Loc_Unknown",
                  'Running', 'Chasing', 'Climbing', 'Eating', 'Foraging', 'Other_Activities', 'Kuks', 'Quaas', 'Moans', 
                  'Tail_flags', 'Tail_twitches', 'Approaches', 'Indifferent', 'Runs_from', 'Other_Interactions']
row_length = len(output_columns) # 38


out_df = pd.DataFrame(columns=output_columns)
## before re-read the df from csv, good idea to cast all datatype to boolean
## df = df.astype(bool)
output_file_path = 'data_mapped.csv'
## process each row to map into a boolean dataset
for i,row in df.iterrows():
  # a new empty dic, if filled, will be injected into the out_df
  empty_dict = dict.fromkeys(output_columns)
  x = 0

  for index, cell in row.items():
    # print(index)
    # print(cell)
    # for location

    # depends on the x y coordinates, the park will be sectioned into
    # upperwest, uppereast, lowereast, lowerwest
    if index == 'x':
      #combine with y to determine the location
      if cell == '':
        break
      x = cell
      continue
    if index == 'y':
      empty_dict['Upperwest'] = False
      empty_dict['Uppereast'] = False
      empty_dict['Lowerwest'] = False
      empty_dict['Lowereast'] = False
      if cell == '':
        break
      if x <= x_mid:
        if cell >= y_mid:
          empty_dict['Upperwest'] = True
        else:
          empty_dict['Uppereast'] = True
      else:
        if cell >= y_mid:
          empty_dict['Lowerwest'] = True
        else:
          empty_dict['Lowereast'] = True
      continue
    
    # for shift
    if index == 'shift':
      empty_dict['AM'] = False
      empty_dict['PM'] = False
      if cell == "AM":
        empty_dict['AM'] = True
      elif cell == 'PM':
        empty_dict['PM'] = True
      else:
        break
      continue
    
    # for age
    if index == 'age':
      empty_dict['Unkown_Age'] = False
      empty_dict['Juvenile'] = False
      empty_dict['Adult'] = False

      if cell == "Adult":
        empty_dict['Adult'] = True
      elif cell == 'Juvenile':
        empty_dict['Juvenile'] = True
      else:
        empty_dict['Unkown_Age'] = True
      continue

    # for main color of the sqr
    # nan 'Gray' 'Cinnamon' 'Black
    if index == 'primary_fur_color':
      empty_dict['Main_Gray'] = False
      empty_dict['Main_Cinnamon'] = False
      empty_dict['Main_Black'] = False
      empty_dict['Main_Other_Color'] = False
      if cell == 'Gray':
        empty_dict['Main_Gray'] = True
      elif cell == 'Cinnamon':
        empty_dict['Main_Cinnamon'] = True
      elif cell == 'Black':
        empty_dict['Main_Black'] = True
      else:
        empty_dict['Main_Other_Color'] = True
      continue
    
    # for hightlight color
    # [nan 'Cinnamon' 'White' 'Gray' 'Cinnamon, White' 'Gray, White'
    # 'Black, Cinnamon, White' 'Black' 'Black, White' 'Black, Cinnamon']
    # 'HL_Cinnamon', 'HL_White', 'HL_Gray', 'HL_Cinnamon_White', 'HL_Gray_White', 'HL_Black_Cinnamon_White', 'HL_Black', 'HL_Black_White', 'HL_Black_Cinnamon', 'HL_Other'

    if index == 'highlight_fur_color':
      empty_dict['HL_Cinnamon'] = False
      empty_dict['HL_White'] = False
      empty_dict['HL_Gray'] = False
      empty_dict['HL_Cinnamon_White'] = False
      empty_dict['HL_Gray_White'] = False
      empty_dict['HL_Black_Cinnamon_White'] = False
      empty_dict['HL_Black'] = False
      empty_dict['HL_Black_White'] = False
      empty_dict['HL_Black_Cinnamon'] = False
      empty_dict['HL_Other'] = False

      if cell == 'Cinnamon':
        empty_dict['HL_Cinnamon'] = True
      elif cell == 'White':
        empty_dict['HL_White'] = True
      elif cell == 'Gray':
        empty_dict['HL_Gray'] = True
      elif cell == 'Cinnamon, White':
        empty_dict['HL_Cinnamon_White'] = True
      elif cell == 'Gray, White':
        empty_dict['HL_Gray_White'] = True
      elif cell == 'Black, Cinnamon, White':
        empty_dict['HL_Black_Cinnamon_White'] = True
      elif cell == 'Black':
        empty_dict['HL_Black'] = True
      elif cell == 'Black, White':
        empty_dict['HL_Black_White'] = True
      elif cell == 'Black, Cinnamon':
        empty_dict['HL_Black_Cinnamon'] = True
      else:
        empty_dict['HL_Other'] = True
      continue

    # for ground location
    if index == 'location':
      empty_dict['Above_Ground'] = False
      empty_dict['Grond_Plane'] = False
      empty_dict['Ground_Loc_Unknown'] = False
      
      if cell == 'Above Ground':
        empty_dict['Above_Ground'] = True
      elif cell == 'Ground Plane':
        empty_dict['Grond_Plane'] = True
      else:
        empty_dict['Ground_Loc_Unknown'] = True
      continue

    # for activities
    if index == 'running':
      empty_dict['Running'] = cell
      continue

    if index == 'chasing':
      empty_dict['Chasing'] = cell
      continue

    if index == 'climbing':
      empty_dict['Climbing'] = cell
      continue

    if index == 'eating':
      empty_dict['Eating'] = cell
      continue

    if index == 'foraging':
      empty_dict['Foraging'] = cell
      continue

    if index == 'other_activities':
      if bool(cell):
        empty_dict['Other_Activities'] = False
      else:
        empty_dict['Other_Activities'] = True
      continue

    # for interactions
    # 'Kuks', 'Quaas', 'Moans', 'Tail_flags', 'Tail_twitches', 'Approaches', 'Indifferent', 'Runs_from', 'Other_Interactions'
    if index == 'kuks':
      empty_dict['Kuks'] = cell
      continue
    if index == 'quaas':
      empty_dict['Quaas'] = cell
      continue
    if index == 'moans':
      empty_dict['Moans'] = cell
      continue
    if index == 'tail_flags':
      empty_dict['Tail_flags'] = cell
      continue
    if index == 'tail_twitches':
      empty_dict['Tail_twitches'] = cell
      continue
    if index == 'approaches':
      empty_dict['Approaches'] = cell
      continue
    if index == 'indifferent':
      empty_dict['Indifferent'] = cell
      continue
    if index == 'runs_from':
      empty_dict['Runs_from'] = cell
      continue

    if index == 'other_interactions':
      if bool(cell):
        empty_dict['Other_Interactions'] = False
      else:
        empty_dict['Other_Interactions'] = True
      continue

  # print(empty_dict)
  # out_df = out_df.append(empty_dict, ignore_index=True)
  new_row = [empty_dict]
  out_df = pd.concat([out_df, pd.DataFrame(new_row)], ignore_index=True)

## write the new row into the INTEGRATED-DATASET.csv
out_df.to_csv(output_file_path, index=False)