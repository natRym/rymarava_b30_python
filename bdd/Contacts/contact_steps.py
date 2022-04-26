from pytest_bdd import given, when, then, parsers
from model.contact import Contact

import random


# +++++++++++++++++++++++++++Test Add new contact+++++++++++++++++++++++++++++++++

@given('a contact list')
def contact_list(db):
    return db.get_contact_list()


@given(parsers.parse('a contact with {firstname}, {lastname} and {middlename}'), target_fixture='new_contact')
def new_contact(firstname, lastname, middlename):
    return Contact(firstname=firstname, lastname=lastname, middlename=middlename)


@when('I add the contact to the list')
def add_new_contact(app, new_contact):
    app.contact.create(new_contact)


@then('the new contact list is equal to the old list with the added contact')
def verify_contact_added(db, contact_list, new_contact):
    old_contacts = contact_list
    new_contacts = db.get_contact_list()
    old_contacts.append(new_contact)
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)


# +++++++++++++++++++++++++++Test Delete a contact+++++++++++++++++++++++++++++++++
@given('non-empty contact list', target_fixture='non-empty contact list')
def non_empty_contact_list(db, app):
    if len(db.get_contact_list()) == 0:
        app.contact.create(Contact(firstname="First Contact"))
    return db.get_contact_list()


@given('a random contact from the list', target_fixture='random_contact')
def random_contact(non_empty_contact_list):
    return random.choice(non_empty_contact_list)


@when('I delete the contact from the list')
def delete_contact(app, random_contact):
    app.contact.delete_contact_by_id(random_contact.id)


@then('the new contact list is equal to the old list without deleted contact')
def verify_contact_deleted(db, non_empty_contact_list, random_contact, app, check_ui):
    old_contacts = non_empty_contact_list
    new_contacts = db.get_contact_list()
    assert len(old_contacts) - 1 == len(new_contacts)
    old_contacts.remove(random_contact)
    assert old_contacts == new_contacts
    if check_ui:
        assert sorted(new_contacts, key=Contact.id_or_max) == sorted(app.contact.contact_list(), key=Contact.id_or_max)

