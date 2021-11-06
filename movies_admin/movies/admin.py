from django.contrib import admin
from .models import Filmwork, Genre, Person

class GenresInlineAdmin(admin.TabularInline):
    model = Filmwork.genres.through
    extra = 0

class PersonRoleInline(admin.TabularInline):
    model = Filmwork.persons.through
    extra = 0

@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    # отображение полей в списке
    list_display = ('title', 'type', 'creation_date', 'rating',)

    # фильтрация в списке
    list_filter = ('type', )

    # поиск по полям
    search_fields = ('title', 'description', 'id',)

    # порядок следования полей в форме создания/редактирования
    fields = (
        'title', 'type', 'description', 'creation_date', 'certificate',
        'file_path', 'rating'
    )

    inlines = (GenresInlineAdmin, PersonRoleInline)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    # отображение полей в списке
    list_display = ('full_name', )

    # поиск по полям
    search_fields = ('full_name', 'id',)

    # порядок следования полей в форме создания/редактирования
    fields = (
        'full_name', 'birth_date'
    )

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    # отображение полей в списке
    list_display = ('name', )

    # поиск по полям
    search_fields = ('name', 'description', 'id',)

    # порядок следования полей в форме создания/редактирования
    fields = (
        'name', 'description'
    )