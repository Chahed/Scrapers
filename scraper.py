from bs4 import BeautifulSoup
from urllib import urlopen
import scraperwiki

def convertirUrl(url):
    l= url.split('/')
    newurl= l[0]+'//'+l[2]
    return newurl

def id_url(url):
    list= url.split('/')
    return (list[len(list)-1])

def listUrl(url):

    response = urlopen(url)
    htmltext = BeautifulSoup(response)

    NewUrl=convertirUrl(url)
    soop = htmltext.find('div',{"class":"contract_set clearfix"})
    links = soop.find_all('a')
    href=[]
    for i in range(0,len(links)-1):
        if i % 2 == 0 :
            href.append(NewUrl+links[i].get('href'))

    return href


def get_numpages(url):
    response = urlopen(url)
    htmltext = BeautifulSoup(response)

    Liste_page =htmltext.find('div',{"id":"pager"})
    a=Liste_page.findAll('a')
    el= a[len(a)-1].get('href')
    n= el.split('/')
    try :
        num=n[6]
    except :
        num=n[4]
    return num

def suittext(text):
    text=text.replace(", ,","")
    text=text.replace("'","")
    text=text.replace("\\n","")
    text=text.replace("  ","")
    text=text.replace("\\r","")
    text=text.replace("[","")
    text=text.replace("]","")
    return text

def Reference(htmltext):
    REF= htmltext.find('p',{"class":"reference_number"}).text
    REFERENCE= REF.split(' ')
    R=""
    for i in range(1,len(REFERENCE)):
        R=R+" "+REFERENCE[i]
    return R

def Awarding_body_fc(htmltext):
    try:
        Awarding= htmltext.find('div',{"class":"contract_hd_left"})
        Awarding_body_list=Awarding.findAll('a')
        Awarding_body= str(Awarding_body_list[0])
        Awarding_body=BeautifulSoup(Awarding_body).text
    except :
        Awarding1= htmltext.find('div',{"class":"contract_hd_left"})
        Awarding= Awarding1.findAll('p')
        Awarding_list=str(Awarding[1]).split('</strong>')
        Awarding_body= str(Awarding_list[1])
        Awarding_body=BeautifulSoup(Awarding_body).text
    return Awarding_body

def Detail_left_fc(htmltext):
    Detail_left=str(htmltext.find('div',{"class":"detail_left"}).contents)
    a=Detail_left.split('<h4>')
    Description=a[1].split('</h4>')
    Description= Description[1]
    Description=BeautifulSoup(Description).text
    Description=suittext(Description)
    return Description

def Table(htmltext,id) :
    Tr=htmltext.find('table',{"class":"additional_data"}).findNext('tbody')
    Table=Tr.findAll('td')
    return str(Table[id])

def Contact(htmltext):
    Contact_Details= str(htmltext.find('div',{"class":"highlight_contact_bd"}).findNext('p').contents)
    c=Contact_Details.split('<br/>')
    m= c[0]+c[1]
    m=BeautifulSoup(m).text
    m=suittext(m)
    return m



def scrap_live(url):
    response = urlopen(url)
    htmltext = BeautifulSoup(response)

    ID=id_url(url)

    REFERENCE= Reference(htmltext)

    Title =htmltext.find('div',{"class":"contract_hd_left"}).findNext('h1').text

    Awarding_body= Awarding_body_fc(htmltext)

    Description= Detail_left_fc(htmltext)

    Contract_Type =BeautifulSoup(Table(htmltext,0)).text
    Procurement_Process =suittext(BeautifulSoup(Table(htmltext,1)).text)
    Estimated_Value_TEXT_DESCRIPTION =suittext(Table(htmltext,2))
    Cat =suittext(Table(htmltext,3))
    Category= (BeautifulSoup(Cat).text).split(',')
    Category=str(Category)
    CPV_codes =suittext(BeautifulSoup(Table(htmltext,4)).text)
    Suitable_for_SME =suittext(BeautifulSoup(Table(htmltext,5)).text)

    Document =htmltext.findAll('div',{"class":"highlight_date_body"})
    Contact_Details=suittext(Contact(htmltext))

    Email = htmltext.find('div',{"class":"c_email"}).text

    DOCUMENT_AVAILABLE_UNTIL= suittext(BeautifulSoup(Document[0].getText()).text)
    SUBMISSION_RETURN_BY= suittext(BeautifulSoup(Document[0].getText()).text)



    data={"ID":unicode(ID), \
          "Url":unicode(url),\
          "REFERENCE":unicode(REFERENCE),\
          "Title":unicode(Title),\
          "Awarding body":unicode(Awarding_body),\
          "Description":unicode(Description),\
          "Contract Type":unicode(Contract_Type),\
          "Procurement Process":unicode(Procurement_Process),\
          "Estimated Value TEXT DESCRIPTION":unicode(Estimated_Value_TEXT_DESCRIPTION),\
          "Category":unicode(Category),\
          "CPV codes":unicode(CPV_codes),\
          "Suitable for SME":unicode(Suitable_for_SME),\
          "DOCUMENT AVAILABLE UNTIL":unicode(DOCUMENT_AVAILABLE_UNTIL),\
          "SUBMISSION RETURN BY":unicode(SUBMISSION_RETURN_BY),\
          "Contact Details":unicode(Contact_Details),\
          "Email":unicode(Email),\
          "Option to extend":unicode(),\
          "EXISITING CONTRACT END DATE":unicode() ,\
          "Start Date":unicode(),\
          "End Date":unicode(),\
          "Date Awarded":unicode(),\
          "Awarded To":unicode()}
    scraperwiki.sqlite.save(unique_keys=['ID'], data=data)


def scrap_awarded(url):
    response = urlopen(url)
    htmltext = BeautifulSoup(response)

    ID=id_url(url)
    REFERENCE= Reference(htmltext)

    Title =htmltext.find('div',{"class":"contract_hd_left"}).findNext('h1').contents
    Title=str(Title)
    Title=BeautifulSoup(Title).text
    Title=suittext(Title)
    Awarding_body= Awarding_body_fc(htmltext)

    Description= Detail_left_fc(htmltext)

    try:
        Startdate =BeautifulSoup(Table(htmltext,0)).text
    except:
        Startdate="none"
    try :
        Enddate =suittext(BeautifulSoup(Table(htmltext,1)).text)
    except:
        Enddate = "none"
    try:
        CPV_codes =suittext(BeautifulSoup(Table(htmltext,2)).text)
    except:
        CPV_codes ="none"

    Date_awarded= htmltext.find('div',{"class":"highlight_date_body"}).text
    Awarded_to= htmltext.find('div',{"class":"highlight_contact_hd"}).findNext('p').contents
    Awarded_to=str(Awarded_to)
    Awarded_to=BeautifulSoup(Awarded_to).text
    Awarded_to=suittext(Awarded_to)



   
    data={"ID":unicode(ID), \
          "Url":unicode(url),\
          "REFERENCE":unicode(REFERENCE),\
          "Title":unicode(Title),\
          "Awarding body":unicode(Awarding_body),\
          "Description":unicode(Description),\
          "Contract Type":unicode(""),\
          "Procurement Process":unicode(""),\
          "Estimated Value TEXT DESCRIPTION":unicode(""),\
          "Category":unicode(""),\
          "CPV codes":unicode(CPV_codes),\
          "Suitable for SME":unicode(""),\
          "DOCUMENT AVAILABLE UNTIL":unicode(""),\
          "SUBMISSION RETURN BY":unicode(""),\
          "Contact Details":unicode(""),\
          "Email":unicode(""),\
          "Option to extend":unicode(""),\
          "EXISITING CONTRACT END DATE":unicode(""),\
          "Start Date":unicode(Startdate),\
          "End Date":unicode(Enddate),\
          "Date Awarded":unicode(Date_awarded),\
          "Awarded To":unicode(Awarded_to)}
    scraperwiki.sqlite.save(unique_keys=['ID'], data=data)

def scrap_recurring(url):
    response = urlopen(url)
    htmltext = BeautifulSoup(response)
    ID=id_url(url)
    REFERENCE= Reference(htmltext)

    Title =htmltext.find('div',{"class":"contract_hd_left"}).findNext('h1').contents
    Title=str(Title)
    Title=BeautifulSoup(Title).text
    Title=suittext(Title)
    Awarding_body= Awarding_body_fc(htmltext)

    Description= Detail_left_fc(htmltext)
    try:
        Contract_Type =BeautifulSoup(Table(htmltext,0)).text
    except:
        Contract_Type="none"
    try:
        Option_to_extend =suittext(BeautifulSoup(Table(htmltext,1)).text)
    except:
        Option_to_extend="none"
    try:
        CPV_codes =suittext(BeautifulSoup(Table(htmltext,2)).text)
    except :
        CPV_codes="none"

    EXISITING_CONTRACT_END_DATE= htmltext.find('div',{"class":"highlight_date_body"}).text

   
     data={"ID":unicode(ID), \
          "Url":unicode(url),\
          "REFERENCE":unicode(REFERENCE),\
          "Title":unicode(Title),\
          "Awarding body":unicode(Awarding_body),\
          "Description":unicode(Description),\
          "Contract Type":unicode(Contract_Type),\
          "Procurement Process":unicode(""),\
          "Estimated Value TEXT DESCRIPTION":unicode(""),\
          "Category":unicode(""),\
          "CPV codes":unicode(CPV_codes),\
          "Suitable for SME":unicode(""),\
          "DOCUMENT AVAILABLE UNTIL":unicode(""),\
          "SUBMISSION RETURN BY":unicode(""),\
          "Contact Details":unicode(""),\
          "Email":unicode(""),\
          "Option to extend":unicode(Option_to_extend),\
          "EXISITING CONTRACT END DATE":unicode(EXISITING_CONTRACT_END_DATE),\
          "Start Date":unicode(""),\
          "End Date":unicode(""),\
          "Date Awarded":unicode(""),\
          "Awarded To":unicode("")}
    scraperwiki.sqlite.save(unique_keys=['ID'], data=data)


def extract_data(url):
    l = ["awarded","recurring","live"]
    for el in l:
        urltry=url
        if el =="awarded":
            urltry=urltry+ "contracts/awarded/type/awarded/page/"
        else :
            if el=="recurring":
                urltry=urltry+"contracts/recurring/type/recurring/page/"
            else :
                urltry=urltry+"contracts/live/page/"
        link = urltry+"1"
        numb= get_numpages(link)
        print (numb)
        for i in range(1,int(numb)+1):
            url2=urltry+str(i)
            List= listUrl(url2)
            for j in List:
                if el=="awarded":
                    scrap_awarded(j)
                else :
                    if el=="live":
                        scrap_live(j)
                    else :
                        if el=="recurring":
                            scrap_recurring(j)



def main():
    urls=["http://www.sourcederbyshire.co.uk/","http://www.sourceleicestershire.co.uk/","http://www.sourcelincolnshire.co.uk/","http://www.sourcenorthamptonshire.co.uk/","http://www.sourcenottinghamshire.co.uk/","http://www.sourcerutland.co.uk/","http://www.sourcecambridgeshire.co.uk/"]
    for url in urls :
        try:
            extract_data(url)
        except:
            pass


if __name__ == '__main__':
    main()
