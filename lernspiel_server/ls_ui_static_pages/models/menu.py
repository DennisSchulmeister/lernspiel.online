# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from typing                             import Optional
from django.db                          import models
from django.urls                        import reverse
from django.utils.translation           import gettext_lazy as _
from lernspiel_server.utils             import models as db_utils

class Menu(db_utils.UUIDMixin, db_utils.CreatedModifiedByMixin):
    """
    A menu contains a number of sections and menu entries, linking to other parts
    of the application.
    """
    name = models.CharField(_("Name"), max_length=255, blank=False)

    def get_translations(self, language: str = "") -> Optional[models.Model]:
        return db_utils.get_translations(self, language)

    class Meta:
        verbose_name        = _("Menu")
        verbose_name_plural = _("Menus")
        ordering            = ["name"]

        indexes = [
            models.Index(fields=["name"])
        ]

    def __str__(self):
        return self.name

    def entries(self):
        """
        Returns a list of all visible menu entries. Instead of model instances a list of
        dictionaries is returned. This contains the sections and their menu entries.

         * `title`:   Section title (if any) 
         * `entries`: List with menu entries of that section
           - `title`:  Link text
           - `type`:   Link type: "none", "url", "page", "view"
           - `target`: HTML `target` attribute
           - `href`:   HTML `href` attribute
        """
        first_entry = True

        sections = [{
            "title":   "",
            "entries": [],
        }]

        for menu_entry in self.menu_entries.order_by("position"):
            translations = menu_entry.get_translations()

            entry_dict = {
                "title":  translations.title if translations else menu_entry.name,
                "type":   menu_entry.link_type,
                "target": "_blank" if menu_entry.new_window else "",
                "href":   "",
                "model":  None,
            }

            match menu_entry.link_type:
                case menu_entry.NONE:
                    if first_entry:
                        sections[-1]["title"] = entry_dict["title"]
                    else:
                        sections.append({
                            "title":   entry_dict["title"],
                            "entries": []
                        })

                    continue
                case menu_entry.URL:
                    entry_dict["href"] = menu_entry.link_url
                case menu_entry.PAGE:
                    if not menu_entry.link_page:
                        continue
                    if not menu_entry.link_page.is_published():
                        continue

                    entry_dict["href"] = menu_entry.link_page.get_published_url()
                case menu_entry.BUILTIN:
                    args = []

                    if menu_entry.link_view_par1:
                        args.append(menu_entry.link_view_par1)
                    if menu_entry.link_view_par2:
                        args.append(menu_entry.link_view_par2)
                    if menu_entry.link_view_par3:
                        args.append(menu_entry.link_view_par3)
                    if menu_entry.link_view_par4:
                        args.append(menu_entry.link_view_par4)
                    if menu_entry.link_view_par5:
                        args.append(menu_entry.link_view_par5)
                    
                    entry_dict["href"] = reverse(menu_entry.link_view_name, args=args)

            sections[-1]["entries"].append(entry_dict)
            first_entry = False

        return sections

class Menu_T(db_utils.UUIDMixin):
    parent   = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="translations")
    language = db_utils.LanguageField()
    title    = models.CharField(verbose_name=_("Title"), max_length=255)

    class Meta:
        verbose_name        = _("Translation")
        verbose_name_plural = _("Translations")
        ordering            = ["parent", "language"]
        indexes             = [models.Index(fields=["parent", "language"])]

    def __str__(self):
        return self.title
