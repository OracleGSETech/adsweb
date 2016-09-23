from splinter import Browser
from selenium import webdriver
import json, sys

executable_path = {'executable_path':'PhantomJS\\bin\\phantomjs.exe'}

class form_filler(object):

	def loadJson(self):
		with open('values.json') as json_file:
			self.values = json.load(json_file); print "Recovering data from JSON file."
		return self.values
        
	def fillForm(self, ticket, ticket_type):
		self.ticket = ticket
		self.ticket_type = ticket_type
		with Browser('phantomjs', **executable_path) as browser:
			ssousername = self.values["Credentials"][0]["Username"]
			password = self.values["Credentials"][0]["Password"]
			sso_url='https://demo.oracle.com'; print "Logging in with user:", ssousername
			ticket_url = 'https://adsweb.oracleads.com/apex/f?p=GO:PAGE:0:TKT:::ID,FWD:'+ str(ticket) +',Y'
			if ssousername <> '' and password <> '':
                                browser.visit(sso_url)
                        else:
                                print 'Please add your username and password.'
                                sys.exit()
			while True:
				if browser.is_text_present('Integrated Cloud Applications and Platform Services'):
					browser.fill('ssousername', ssousername)
					browser.fill('password', password)
					browser.find_by_css('a.submit_btn').first.click(); print "SSO login successful."
				elif browser.is_text_present('Search the Demo Store'):
					browser.visit(ticket_url); print "Filling up fields."

					if self.values[ticket_type][0]["Resolution Type"] <> '':
                                                browser.find_option_by_text(self.values[ticket_type][0]["Resolution Type"]).first.click()
                                        else:
                                                print 'Resolution Type empty. Will not select from list.'

                                        if self.values[ticket_type][0]["Status"] <> '':
                                                browser.find_option_by_text(self.values[ticket_type][0]["Status"]).first.click()
                                        else:
                                                print 'Status is empty, will not fill the field.'

					if self.values[ticket_type][0]["Assignee"]<> '':
                                                browser.find_option_by_text(self.values[ticket_type][0]["Assignee"]).first.click()
                                        else:
                                                print 'Assignee is empty. Will not select from list.'

					if self.values[ticket_type][0]["Resolution"] <> '':
                                                try:
                                                        browser.fill('p_t24', self.values[ticket_type][0]["Resolution"])
                                                except:
                                                        pass
                                                try:
                                                        browser.fill('p_t25', self.values[ticket_type][0]["Resolution"])
                                                except:
                                                        pass
                                        else:
                                                print 'Resolution is empty, will not fill the field.'

                                        if self.values[ticket_type][0]["Description"] <> '':      
                                                try:
                                                        browser.fill('p_t96',self.values[ticket_type][0]["Description"])
                                                except:
                                                        pass
                                                try:
                                                        browser.fill('p_t97',self.values[ticket_type][0]["Description"])
                                                except:
                                                        pass
                                        else:
                                                print 'Description is empty, will not fill the field.'
                                                
					browser.find_by_id('UPDATE_TICKET').first.click(); print "Ticket", ticket, "successfully updated."
					browser.quit()
					sys.exit()
				else:
					continue


if len(sys.argv) == 3:
        if  len(sys.argv[1])==6 and sys.argv[1].isdigit():
                my_ff = form_filler()
                
                try:
                        my_ff.loadJson()
                except ValueError:
                        print "Please verify the validity of json at http://jsonlint.com/ "
                        sys.exit()     
                try:
                        my_ff.fillForm(sys.argv[1], sys.argv[2])
                except KeyError as ke:
                        print 'Error: Please verify the json category.\n',sys.argv[2],'category not found.'
                except SystemExit as se:
                        print 'Exiting program.'
                except:
                        print "Unexpected error:", sys.exc_info()[0]
        else:
                print 'Invalid ticket number.'
else:
        print "You need to specify the ticket number and a JSON category"
        print "Usage: adsweb ticket_number json_category"

