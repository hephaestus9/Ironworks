# -*- coding: utf-8 -*-
from mechanize import ParseResponse, urlopen, urljoin


class ShowRss():

    def __init__(self):
        self.uri = 'http://showrss.karmorra.info'
        self.page = None

    def login(self, username, password):
        response = urlopen(urljoin(self.uri, "/?cs=login"))
        forms = ParseResponse(response, backwards_compat=False)
        form = forms[0]
        form.set_value(username, name='username')
        form.set_value(password, name='password')
        self.page = urlopen(form.click())

    def getShowsList(self):
        #returns dict of {id, show} and keys
        forms = ParseResponse(self.page, backwards_compat=False)
        selectList = forms[1]
        control = selectList.controls[0]
        listValues = [item.attrs['value'] for item in control.items]
        listLabels = [item.attrs['label'] for item in control.items]
        #right now this works, but I think it is just lucky -- there may be sorting issues
        showList = {}
        i = 0
        for item in listValues:
            showList[item] = listLabels[i]
            i += 1

        keys = listValues

        return showList, keys