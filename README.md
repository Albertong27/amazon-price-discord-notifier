# Amazon Price Discord Notifier
Get a notification through Discord when your wanted item price drop bellow configured threshold! \
Any contribution are welcome !
## Features
- Out of stock detection
- Store the historical price
- Support Multi item
- Ability to set the threshold price for each item

## Usage
### !add {url} 
Adding new item to track.
### !remove {id}
Remove item with specific id.
### !list
List all tracked items.
### !threshold {id} {price threshold}
Set the threshold for the specific item id.
### !history {id}
Show the historical data for the specific id.
### !ping
Will return Pong!, nothing else..
##
Warning: Current version does not support multi user and only support SGD(Singapore Dollar).
## TO-DOs
- [ ] Add multiuser support
- [ ] Add support for multi-currency
- [ ] Fix issue with the out of stock detection
