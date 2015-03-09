from django.db import models
from Helpdesk.models import DocNumber

class DocNumberManager(models.Manager):
    def create(self, docType, year, month):
        DocNumber = self.model(
            docType = docType,
            year = year,
            month = month,
            lastNumber = 0
        )
        DocNumber.save(using=self._db)
        return DocNumber
    
    def update(self, docType, year, month, lastNumber):
        docNumber = DocNumber.objects.get(docType=docType, year=year, month=month)
        docNumber.lastNumber = lastNumber
        docNumber.save(using=self._db)
        return docNumber
    
    def getMaxNo(self, docType, year, month):
        docNumber = DocNumber.objects.filter(docType=docType, year=year, month=month)
        if docNumber.count() != 0:
            return DocNumber.lastNumber
        else:
            self.create(self, docType, year, month)
            return 0
            
    def createNo(self, docType, year, month):
        maxNo = self.getMaxNo(self, docType, year, month) + 1
        self.update(self, docType, year, month, maxNo)
        return docType+""+docType[2:2]+""+month+"%04d" % self.max_no;
    
    
class TicketNumberManager(models.Manager):
    def create(self, docType, year, month):
        DocNumber = self.model(
            docType = docType,
            year = year,
            month = month,
            lastNumber = 0
        )
        DocNumber.save(using=self._db)
        return DocNumber
    
    def update(self, docType, year, month, lastNumber):
        docNumber = DocNumber.objects.get(docType=docType, year=year, month=month)
        docNumber.lastNumber = lastNumber
        docNumber.save(using=self._db)
        return docNumber
    
    def getMaxNo(self, docType, year, month):
        docNumber = DocNumber.objects.filter(docType=docType, year=year, month=month)
        if docNumber.count() != 0:
            return DocNumber.lastNumber
        else:
            self.create(self, docType, year, month)
            return 0
            
    def createNo(self, docType, year, month):
        maxNo = self.getMaxNo(self, docType, year, month) + 1
        self.update(self, docType, year, month, maxNo)
        return docType+""+docType[2:2]+""+month+"%04d" % self.max_no;
    
    
