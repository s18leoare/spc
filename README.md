# spc
Statistical Process Control Web

Possibly future business idea.  "Intelligent Process Control"

## To do
### Expandable structure
Currently only written as a static sheet - need to get the nav bar and aside to be inserted without repeating code.  Need to approiach a modular stucture where it is easy to ad new data sources without re-making a page every time.

- [x] Change to flask server with embedded dash pages
- [ ] Mutable attribute choices
- [ ] Create database structure for data storage
    - [ ] standard extraction
    - [ ] Importer (ideally with the web site) 
- [ ] Nav bar and aside in re-usable code
- [x] Add virtual environment
- [x] auto flask environment variable to be able to `flask run` from cmd

### Base design
- [x] Histogram on main chart
- [ ] Change graphing functions to python syntax
- [ ] Capability metrics
- [ ] Specification lines on main plots
- [ ] Weekly / monthly / annual / custom trends and capabilities
- [ ] Download data button
- [ ] Modelling section - inputs vs outputs
    - [ ] Scatter plot
    - [ ] Clustering / unsupervised
    - [ ] Model application (large section - expend when working on it)