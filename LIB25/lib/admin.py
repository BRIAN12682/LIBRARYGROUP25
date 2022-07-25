from django.contrib import admin
from .models import User, Area, SubArea, Books, Students, IssueBook, UserProfile, chatMessages, FinedStudents, IssuedBook


# Register your models here.
admin.site.register(User),
admin.site.register(Area),
admin.site.register(SubArea),
admin.site.register(IssueBook),
admin.site.register(Books),
admin.site.register(Students),
admin.site.register(UserProfile),
admin.site.register(chatMessages),
admin.site.register(FinedStudents),
admin.site.register(IssuedBook)


