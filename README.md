# Dramatis Personae
This is a multipurpose software designed to help handle Hdi's Fading Suns Tabletop RPG epics. 
- The main application of the project is **Collector**, which purpose is to collect all characters for the campaign.
- **Scenarist** will help prepare notes before and after sessions, with a reference system that allow to link characters from collector to the articles of scenarist.
- **Cartograph** does everything about maps, the Jumpweb in particular.

## Collector
The app storing all characters.

### SVG_SHEET
Common to many tabletop RPG applications. Allow the online creation of characters sheet. This function is implemented 
through the FICS_Sheet child class. Here are a few guildelines on what does what among the many utility functions.

* fillBasics(oy): Start drawing the main info about the character at oy vertical steps. Takes the whole width of the sheet.
* fillAttributes(oy)
