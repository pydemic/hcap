# Region data

- [Region data](#region-data)
  - [Kinds](#kinds)
  - [Continents](#continents)
  - [Countries](#countries)
  - [Brazil](#brazil)
    - [Brazil macroregions](#brazil-macroregions)
    - [Brazil states](#brazil-states)
    - [Brazil mesoregions](#brazil-mesoregions)
    - [Brazil cities](#brazil-cities)
    - [Brazil neighborhoods](#brazil-neighborhoods)

## Kinds

|  ID   | Name         | Description                             |
| :---: | :----------- | :-------------------------------------- |
|   0   | None         | Default and undefined kind              |
|   1   | World        | The entire planet                       |
|   2   | Continent    | A continent                             |
|   3   | Country      | A country                               |
|   4   | Macroregion  | A subset of a country                   |
|   5   | State        | A state                                 |
|   6   | Mesoregion   | A set of cities from one or more states |
|   7   | City         | A city or municipality                  |
|   8   | Neighborhood | A neighborhood                          |

## Continents

- Based on seven-continents model

- `code` is the standard 2-chars english abbreviation of the continent

- `parents` is a single item, related to world

- `parent_hierarchy` is `W`

## Countries

- Based on [ISO-3166](https://www.iso.org/glossary-for-iso-3166.html)

- `code` is the standard 2-digits or 3-digits ISO-3166 numeric code

- `parents` is a single item, related to the region of `kind` "continent"

- `parent_hierarchy` is the continent code

- `abbr` is the standard 2-letters ISO-3166 Alpha-2 code

## Brazil

### Brazil macroregions

- Based on IBGE standard of region

- `code` is the standard 1-digit code of the region

- `parents` is a single item, related to the Brazilian country

- `parent_hierarchy` is `SA:BR`

- `abbr` is the IBGE standard 1-letter or 2-letters for region acronym

### Brazil states

- Based on IBGE standard of federative unit

- `code` is the standard 2-digits code of the state

- `parents` can be related to the Brazilian country

- `parents` can be related to a Brazilian macroregion

- `parent_hierarchy` is `SA:BR`

- `abbr` is the IBGE standard 2-letters for state acronym

### Brazil mesoregions

- Based on IBGE standard of imediate geographic region or intermediate
  geographic region

- `code` can be the standard 4-digits of the intermediate geographic region

- `code` can be the standard 6-digits of the imediate geographic region

- `parents` can be related to the Brazilian country

- `parents` can be related to a Brazilian macroregion

- `parents` can be related to a Brazilian state

- `parent_hierarchy` is `SA:BR:<state_code>`

### Brazil cities

- Based on IBGE standard of municipalities

- `code` is the standard 7-digits of the municipality

- `parents` can be related to a Brazilian state

- `parents` can be related to a Brazilian mesoregion

- `parent_hierarchy` is `SA:BR:<state_code>`

### Brazil neighborhoods

- Currently, Brazil does not have a standard for neighborhoods

- `code` can be the standard 8-digits of a zip code (Brazilian acronym: CEP)

- `code` can be the standard 9-digits of a district, from IBGE

- `code` can be the standard 11-digits of a sub-district or zone, from IBGE

- `parents` can be related to a Brazilian city

- `parents` can be related to other neighborhood (useful if sub-district or
  zone)

- `parent_hierarchy` is `SA:BR:<state_code>:<city_code>`
