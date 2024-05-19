# SPI
OpenCore SPI RTL is verified using COCOTB.
## Running the Tests
### To run Individual Tests:
  `make TESTCASE=<Name_of_TestCase>` 
 Note: Name_of_TestCase can be found in test_spi.py like `async def <<name>>`.Here, name is the TestCase Name
### To run TestFactory
   `make TF_EN=1`
## Generate Code Coverage 
   - `make CVG_EN=1` to generate **coverage.dat** 
   -  Once generated, run `make coverage`  which will display coverage in the terminal.
   -  To view coverage in HTML Format, above step generates the folder called **coverage** which will contain **index.html**
   -  To clean coverage, run `make clean_coverage`
