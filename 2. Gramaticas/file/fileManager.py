import sys
import re

class FileManager:
    def __init__(self, fileName):
        self.fileName = fileName
        self.gramaticData = []

        ## File extension verification.
        def verifyFileExtension():
            pattern = re.compile(r'^[a-z]+[\.{1}]gr$', re.IGNORECASE)
            result = pattern.match(self.fileName)

            try:
                result.group()
            except:
                print('Invalid file extension.')
            
        ## Open file to read
        def openFile():
            def validateLine(content):
                whitoutSpaces = re.sub(r'\s', '', content)

                pattern = re.compile(r'(^<[a-z]+>->(([a-z0-9]+|(<[a-z]+>)+)+|\/{1})$)', re.I)
                result = pattern.match(whitoutSpaces)

                try:
                    self.gramaticData.append(result.group())
                    return True
                except:
                    print('Invalid format.')
                    return False
                
            # Open, read and close the file.
            try:
                file = open(self.fileName)

                # File validation
                lineContent = file.readline()
                while lineContent and validateLine(lineContent):
                    lineContent = file.readline()
            except OSError as e:
                print('Something wrong opening the file.')
                print(e)
            finally:
                try:
                    file.close()
                except OSError as e:
                    print('Finishing execution...')
                    print(e)
                    exit(1)


        # First: Verify the file extension.
        verifyFileExtension()

        # Second: Open the file.
        openFile()


    def fileData(self):
        return self.gramaticData
