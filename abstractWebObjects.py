from abc import ABC, abstractmethod

class WebsiteObject(ABC):
    @abstractmethod
    def getHTML(self):
        pass

    @abstractmethod
    def getJS(self):
        pass

    @abstractmethod
    def getName(self):
        pass

class webUserInput(WebsiteObject, ABC):
    @abstractmethod
    def getValue(self):
        return 0

    @abstractmethod
    def setValue(self, val):
        pass

class webUserValueDisplay(WebsiteObject, ABC):
    @abstractmethod
    def setValue(self, val):
        pass
