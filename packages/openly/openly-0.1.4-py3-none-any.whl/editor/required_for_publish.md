# Requirements for an activity to be publishable

# General Tab

## Title/Description/Objective
    * if no title is set this will look ugly on the activity list ( unless we display 'no title' )
    * if no description/objective is set activity profile about tab will look empty    

     enforcing title and description

## Dates
    * if no dates are set, currently activity will not show up on the site 
        we could enforce one start date before publish
    * if dates are set incorrectly form will show errors on submit
    
     enforcing one start date

## Status
    * used in profile page and dashboard charts

     enforcing status 

## Collaboration Type
    * not used at all in openly at present

# Sectors

## Sector & Sector Working Group
    * lack of sectors will mean activity does not show up in sector dashboard

     enforcing one sector to be chosen

## Policy markers
    * not required as far as i can see


# Participating Organisations
    * Funding Orgs used by total_donor charts in dashbaords
    * Implementing Orgs displayed in activity profile
    * Accountable Orgs used for ministry filter

    not required

# Locations
    * used for location dashboard
    * if not defined will be displayed in all location filter pages, but will not contribute to commitment by location charts

    enforce and default to Nationwide

# Finances

## General
    * nothing required
## Budgets
    * nothing currently used
    * if an activity has no transactions these might be relevant though - but not currently used
## Transactions
    * used heavily - if none are present, the activity will have no financial data used by openly

    enforcing at least one transaction of type commitment

# Results
    * not required
# Contacts
    * not required
