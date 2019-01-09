from django.db import models

class model_books(models.Model):
    book_name   = models.CharField(max_length=100)
    book_author = models.CharField(max_length=100)
    release_date = models.DateField(null=True)
      
    def __str__(self):
        return self.book_name

    class Meta:
        db_table = "model_books"    

class model_chapters(models.Model):
    chapter_number = models.IntegerField()
    chapter_name = models.CharField(max_length=100)
    model_booksid = models.ForeignKey(model_books, related_name="book_chapters", on_delete=models.CASCADE)  
      
    def __str__(self):
        return self.chapter_number

    class Meta:
        db_table = "model_chapters"                   

class model_page(models.Model):
    page_content = models.CharField(max_length=1000)
    model_chaptersid = models.ForeignKey(model_chapters, related_name="chapters_page", on_delete=models.CASCADE)  
      
    def __str__(self):
        return self.page_content

    class Meta:
        db_table = "model_page"            