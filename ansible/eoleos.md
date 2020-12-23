AirShield+ Exchanged files formatting
===


## Multidirectional files <a name='multi'></a> [<i class='fa fa-angle-double-up fa-xs'></i>](#root)
### CPE Lifecycle (End of Life / End of Service bulk update) <a name='eoleos'></a>
- **Description**: This file is uploaded with the command `airshield-admin cpe_lifecycle`. It is meant to upload/download bulk lifecycle information about
the CPE EoL/EoS.
- **File Format**: plain text (see **Rules** below for formatting quirks)
- **Actual command**:
```bash
# Template
airshield-admin cpe_lifecycle {eol|eos} {import|export} {file}

# Import EoL example
ROOT> airshield-admin cpe_lifecycle eol import eolsourcefile.txt

# Export EoS example
ROOT> airshield-admin cpe_lifecycle eos export extracteos.txt
```

- **Rules**
	- It is not possible to mix *EoL* and *EoS* data in the same file. The command line tool addresses one specific kind of information according to the parameter selected. Be aware not to mix EoL/EoS informations in the ressource file.
	- The information EoL or EoS dealt with for the full file is given in the command line.
	- It is not possible to address both import and export in the same file.
	- A blank line posts the current job and resets the parameters
	- A comment line, starting with a dash symbol *(\#)* is ignored.
	- A line containing a well formatted datetime set the *EoL/EoS* information for the current job.
	- A line containing a cpe *URI2_3* name adds this CPE to the current job (starting with cpe:/)
	- A line not empty, not commented, not defining a CPE or not defining a date is considered reference information for the current job.

- **Examples**
```bash
# eolsourcefile.txt
# starting with a blank line resets everything

# Date & Ref (the order do not count as we reseted the parameters with the previous blank line)
2008-12-01 00:00:00
http://www.acme.com/us/support/library/lifecycle-information-666.pdf
# We add the CPe one by one
cpe:/a:acme:not_a_real_cots:1.%0
cpe:/a:acme:not_a_real_cots:1.%03
cpe:/a:acme:not_a_real_cots:1.%04
cpe:/a:acme:not_a_real_cots:1.%07
cpe:/a:acme:not_a_real_cots:1.%08
cpe:/a:acme:not_a_real_cots:2.%01
cpe:/a:acme:not_a_real_cots:2.%07

# The last blank will force a post of the current job job and reset the parameters for the next job
``` 
This example will import inside the airshield instance end of life information (december 1st, 2008) and reference
(http://www.acme.com/us/support/library/lifecycle-information-666.pdf) for the 7 version of the *not_a_real_cots* product by *Acme*. More EoL
import jobs could have been appended to this file, but only for import and concerning *end_of_life* and *end_of_life_reference*. For an
*end_of_service* / *end_of_service_reference* an other file executed with the command parameter *eos* instead of *eol*.

We will note that commented lines are welcome in this file format, but we have to be careful with the blank lines that will explicitly send
a reset.





*	*	*

| [Index](airshield.md) | [Top of document](#root) | <alexandre.guyon@apsys-airbus.com> | End of Document |
| :--- | :---: | :---: | ---: |

	

