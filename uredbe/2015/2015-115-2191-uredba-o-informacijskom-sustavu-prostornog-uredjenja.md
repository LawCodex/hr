---
title: "Uredba o informacijskom sustavu prostornog ure­đenja"
identifier: "NN 115/2015 (2191)"
eli: "https://narodne-novine.nn.hr/eli/sluzbeni/2015/115/2191"
type: decree
jurisdiction: hr
language: hr
date: 2015-10-23
status: in_force
status_basis: "derived: enacted or amended in 2015 and no later repeal, replacement or expiry detected in Narodne novine (not an official in-force list)"
text_version: original
narodne_novine: "115/15"
amendments: []
source: "https://narodne-novine.nn.hr/eli/sluzbeni/2015/115/2191"
retrieved: 2026-10-12
---

# Uredba o informacijskom sustavu prostornog ure­đenja

> Izvor: Narodne novine, NN 115/2015 (https://narodne-novine.nn.hr/eli/sluzbeni/2015/115/2191).
>
> Ovo nije službeni pročišćeni tekst osim ako je gore navedeno; status je utvrđen automatski.

VLADA REPUBLIKE HRVATSKE

Na temelju članka 37. Zakona o prostornom uređenju (»Narodne novine«, broj 153/13), Vlada Republike Hrvatske je na sjednici održanoj 22. listopada 2015. godine donijela

**UREDBU**

**O INFORMACIJSKOM SUSTAVU PROSTORNOG UREĐENJA**

## DIO PRVI — UVODNE ODREDBE

*Predmet Uredbe*

### Članak 1.

Ovom se Uredbom propisuje struktura, sadržaj, način rada, oblik i elektronički standard informacijskog sustava prostornog uređenja, ovlasti i obveze u vođenju i upravljanju tim sustavom, te javnopravna tijela koja su prostorne i druge podatke dužna učiniti dostupnima putem informacijskog sustava prostornog uređenja i način na koji su to dužna učiniti.

*Primjena Uredbe*

### Članak 2.

Pravila propisana ovom Uredbom u vezi s izradom, donošenjem i dostavom prostornog plana na odgovarajući se način primjenjuju i na izradu, donošenje i dostavu izmjena i dopuna prostornog plana.

*Pojmovi*

### Članak 3.

Pojedini pojmovi u ovoj Uredbi imaju sljedeće značenje:

− georeferenciranje je pridruživanje geografskih koordinata ili pravokutnih koordinata u određenoj kartografskoj projekciji pojedinim točkama određenog objekta

− GeoTIFF je elektronički format zapisa koji omogućava da se u digitalni rasterski oblik dokumenta uključe prostorne reference kojima ga je moguće smjestiti na točno definiranu lokaciju u virtualnom prostoru

− GML je jezik za označavanje geografskih objekata temeljen na XML-u (engl. eXtensible Markup Language). Određuje geometriju i svojstva objekata koji čine geografsku informaciju te služi za razmjenu i pohranjivanje prostornih podataka

− interoperabilnost (međudjelovanje) podrazumijeva mogućnost kombiniranja skupova prostornih podataka i međudjelovanje usluga bez ponavljajuće manualne intervencije, tako da je rezultat dosljedan i da je dobivena dodana vrijednost skup podataka i usluga

− internetski servisi za razmjenu podataka podrazumijevaju mrežne usluge za razmjenu prostornih podataka putem standardiziranih protokola poput WMS, WFS i dr.

− metapodaci su podaci o podacima koji opisuju skupove i servise prostornih podataka i omogućavaju njihovo otkrivanje, pregled i uporabu

− Nacionalna infrastruktura prostornih podataka (u daljnjem tekstu: NIPP) je skup tehnologija, mjera, normi, provedbenih pravila, usluga, ljudskih kapaciteta i ostalih čimbenika koji omogućavaju djelotvorno objedinjavanje, upravljanje i održavanje dijeljenja prostornih podataka određenih posebnim zakonom kojim se uređuje NIPP u svrhu zadovoljenja potreba na nacionalnoj, kao i na europskoj razini, a koji će biti sastavni dio europske infrastrukture prostornih podataka (INfrastructure for SPatial InfoRmation in Europe)

− PDF je elektronički format zapisa dokumenata koji se koristi za zapis dvodimenzionalnih dokumenata neovisno o programskom alatu, uređaju i rezoluciji ispisa. PDF format je otvoreni standard objavljen od strane Međunarodne organizacije za normizaciju

− rasterski oblik dokumenta je digitalni zapis grafičkog dokumenta koji za prikaz sadržaja koristi matricu pojedinačnih točaka od kojih svaka ima svoju boju, a koji zapis se pohranjuje u različitim formatima prilagođenim prikazu takve strukture (tiff, jpeg, png i dr.)

− rezolucija digitalnog zapisa grafičkog dokumenta određena je brojem točaka od kojih je sastavljen rasterski oblik dokumenta po kvadratnom inču i izražava se u DPI (engl. Dots Per Inch)

− SHP format je geoprostorni vektorski format otvorene specifikacije za Geografske Informacijske Sustave kojeg je razvio ESRI (Environmental Systems Research Institute) kao format za potrebe prijenosa podataka između vlastitih i drugih programskih paketa

− službena kartografska projekcija HTRS96/TM je koordinatni sustav poprečne Mercatorove (Gauss-Krügerove) projekcije sa srednjim meridijanom 16°00’ i linearnim mjerilom na srednjem meridijanu 0,9999 uz HTRS96 Republike Hrvatske za područje katastra i detaljne državne topografske kartografije

− topološka uređenost prostornih podataka podrazumijeva da su poligoni koji ih opisuju zatvoreni, da se poligoni u istom sloju ne preklapaju međusobno, niti da između njih postoje praznine, te da se linija sastoji od jednog neprekinutog dijela

− vektorski oblik dokumenata je digitalni zapis grafičkih dokumenata u obliku matematičkih funkcija koje opisuju prostorne objekte – elemente prikaza (točke, linije, krivulje i poligone)

− Web Feature Service Interface Standard (WFS) podrazumijeva sučelje za traženje i otkrivanje pojedinačnih prostornih objekata i atributa putem Interneta koristeći pozive neovisne o platformi

− Web Map Service (WMS) je standardni protokol za razmjenu georeferenciranih karata i drugih digitalnih rasterskih dokumenata putem interneta.

## DIO DRUGI — SADRŽAJ, NAČIN RADA, OBLIK, STRUKTURA I ELEKTRONIČKI STANDARD INFORMACIJSKOG SUSTAVA PROSTORNOG UREĐENJA

*Sadržaj, povezivanje i uloga informacijskog sustava prostornog uređenja*

### Članak 4.

(1) Informacijski sustav prostornog uređenja (u daljnjem tekstu: ISPU) je državni interoperabilni i multiplatformni sustav za unos, verifikaciju, javnu objavu i razmjenu prostornih podataka za potrebe izrade, donošenja, provedbe i nadzora prostornih planova, trajnog praćenja stanja u prostoru i području prostornog uređenja, izrade izvješća o stanju u prostoru, te obavljanje poslovnih procesa propisanih zakonom koji uređuje područje prostornog uređenja i posebnim propisima.

(2) U ISPU se povezuju informacijski sustavi javnopravnih tijela koja na temelju zakona kojim se uređuje područje prostornog uređenja i posebnih propisa izrađuju i/ili održavaju prostorne podatke i druge podatke značajne za prostorno uređenje ili sudjeluju u izradi i provedbi prostornih planova.

(3) ISPU-om se osigurava:

− objedinjavanje i razmjena podataka o izradi, donošenju, provedbi i nadzoru prostornih planova

− prikupljanje i objedinjavanje podataka i/ili informacija za izradu prostornih planova, uključivo i povezivanje sustava i internetskih servisa za razmjenu podataka javnopravnih tijela u čijoj su nadležnosti prostorni podaci potrebni za obavljanje ili vođenje poslova iz stavka 1. ovoga članka i

− pristup javnosti podacima i informacijama vezanim uz prostorno uređenje, te ovlaštenim korisnicima u skladu s razinom ovlasti za potrebe prostornog planiranja i praćenja stanja u prostoru.

(4) ISPU se povezuje s geoportalom NIPP-a u cilju omogućavanja pristupa uslugama pronalaženja, pregledavanja, preuzimanja i drugim uslugama NIPP-a.

(5) ISPU je niz međusobno povezanih računalnih aplikacija za prihvat, obradu i prikaz podataka o prostoru iz raznih izvora, koji obuhvaća osobito:

− podatke o postojećem i planiranom načinu korištenja zemljišta (namjeni prostora, uvjetima provedbe zahvata u prostoru i drugim uvjetima korištenja i zaštite prostora) propisanih prostornim planovima i posebnim propisima

− metapodatke o važećim prostornim planovima, prostornim planovima koji su u postupku izrade i donošenja, te o prostornim planovima koji su prestali važiti, do razine propisane ovom Uredbom

− podatke o upravnim i drugim aktima nadležnih tijela koji se izdaju i koji su izdani u svrhu provedbe prostornih planova, građenja, uporabe i uklanjanja građevina

− podatke o približnim vrijednostima zemljišta i druge nužne podatke potrebne za izradu procjene vrijednosti nekretnina

− podatke o sektorskim strategijama, planovima, studijama i drugim dokumentima propisanim posebnim zakonima značajnim za prostorno uređenje i

− druge podatke i informacije od utjecaja na praćenje stanja u prostoru i prostornog uređenja na svim razinama.

*Struktura ISPU-a*

### Članak 5.

(1) ISPU se organizira kao sustav samostalnih funkcionalnih cjelina – modula za unos i verifikaciju podataka koji se mogu međusobno povezivati.

(2) Moduli iz stavka 1. ovoga članka su:

− modul ePlanovi u koji se unose tekstualni i grafički dijelovi elaborata prostornih planova, izrađeni sukladno zakonu koji uređuje područje prostornog uređenja i pravilnikom kojim se propisuje sadržaj prostornih planova, metapodaci kojima se opisuju prostorni planovi tijekom postupka izrade i donošenja te dokumentacija koja prati izradu i donošenje prostornih planova, a služi za održavanje i preuzimanje šifrarnika propisanih pravilnikom kojim se propisuje sadržaj prostornih planova

− modul eKatalog u koji se unose metapodaci kojima se opisuju važeći prostorni planovi i prostorni planovi stavljeni izvan snage za potrebe razmjene s drugim modulima ISPU-a te za pružanje usluga pronalaženja, pregledavanja i preuzimanja prostornih podataka u okviru NIPP-a

− modul eDozvola koji služi za izdavanje akata za provedbu zahvata u prostoru

− modul eInspekcija koji služi za prikaz zahvata u prostoru za koje su donesena izvršna rješenja građevinske inspekcije prema posebnom propisu

− modul eArhiv u koji se unose podaci o aktima za građenje izdani prije uspostave modula eDozvola i metapodaci o njima

− modul eNekretnine koji služi za unos podataka u zbirku kupoprodajnih cijena, te za izradu i prikaz plana približnih vrijednosti zemljišta i izdavanje izvadaka iz plana i zbirke u skladu s posebnim propisom koji uređuje procjenu vrijednosti nekretnina

− ISPU-lokator koji služi za pristup podacima iz svih slojeva od značaja za bilo koju odabranu lokaciju i točno pozicioniranje u prostor oznaka koje opisuju te podatke

− ulazni modul NIPP-a koji služi za prihvat podataka nastalih izvan geoportala ISPU, a koji su od utjecaja na podatke o prostoru.

(3) ISPU je moguće proširivati i drugim modulima od utjecaja na prostorno planiranje i/ili praćenje stanja u prostoru.

*Dostava podataka i registar javnopravnih tijela*

### Članak 6.

(1) Podatke i informacije značajne za prostorno uređenje i izradu prostornih planova javnopravna tijela pripremaju i dostavljaju u ISPU strukturno i sadržajno uređene u skladu s pravilnikom koji propisuje sadržaj prostornih planova.

(2) Popis javnopravnih tijela iz stavka 1. ovoga članka sadržan je u Registru javnopravnih tijela koji je sastavni dio modula eDozvola.

(3) Javnopravna tijela dužna su podatke iz stavka 1. ovoga članka učiniti dostupnima putem internetskih servisa za razmjenu podataka te ih ažurirati sukladno rokovima određenim posebnim propisima kojima se uređuje NIPP.

(4) Internetski servisi za razmjenu podataka moraju biti izrađeni u skladu s posebnim propisima kojima se uređuje NIPP.

(5) Subjekti ISPU-a za korištenje internetskih servisa za razmjenu podataka ne plaćaju naknadu.

*Podaci geodetske izmjere o zahvatima u prostoru*

### Članak 7.

Za potrebe unosa podataka o zahvatima u prostoru u modulu eDozvola ovlašteni inženjeri geodezije i pravne osobe koji obavljaju poslove državne izmjere i katastra nekretnina dužni su dostavljati podatke geodetske izmjere u gml formatu.

*Preuzimanje i razmjena podataka*

### Članak 8.

(1) Subjekti ISPU-a mogu iz ISPU-a preuzeti za korištenje u vlastitim aplikacijama ili za proizvodnju novih prostornih podataka iz svoje nadležnosti podatke, metapodatke i druge informacije iz članka 4. stavka 5. ove Uredbe, putem standardnih internetskih servisa za razmjenu podataka.

(2) Podaci iz ISPU-a se preuzimaju bez naknade.

(3) Subjekti ISPU-a koji su proizveli nove podatke korištenjem podataka preuzetih iz ISPU-a, obvezni su bez naknade te podatke učitati u ISPU ili ih učiniti dostupnima ostalim subjektima na drugi pogodan način.

*Neusklađenost i nedostavljanje podataka*

### Članak 9.

(1) Ako su podaci, odnosno informacije iz članka 6. stavka 1. ove Uredbe međusobno neusklađeni, stručni izrađivač prostornog plana (u daljnjem tekstu: stručni izrađivač) može u dogovoru s nositeljem izrade prostornog plana te u skladu sa smjernicama za izradu plana i koncepcijom plana izraditi planersko rješenje u prijedlogu prostornog plana koristeći međusobno neusklađene podatke, odnosno informacije samo okvirno.

(2) Ako nadležno javnopravno tijelo ne dostavi u propisanom roku podatke, odnosno informacije iz članka 6. stavka 1. ove Uredbe ili podaci ne postoje, stručni izrađivač pri izradi prijedloga prostornog plana može u dogovoru s nositeljem izrade koristiti podatke, odnosno informacije iz drugih odgovarajućih izvora.

*Geoportal ISPU-a*

### Članak 10.

(1) Geoportal ISPU-a je internetska stranica ili njezin ekvivalent koji omogućava prikaz i pregledavanje javno dostupnih prostorno-planskih slojeva i drugih prostornih slojeva, podataka i informacija iz modula ISPU-a i drugih izvora.

(2) Pristup geoportalu ISPU-a je javan, osim modulima iz članka 5. stavka 2. ove Uredbe u dijelu za preuzimanje, unos, povlačenje i/ili verifikaciju podataka.

(3) Geoportalom ISPU-a se ostvaruje i pristup pojedinim modulima iz članka 5. stavka 2. ove Uredbe za ovlaštene korisnike, te se njime omogućava upravljanje prikazom, pretraživanje, te ispis prikazanog sadržaja.

*Način rada ISPU-a*

### Članak 11.

(1) U radu ISPU-a primjenjuju se standardizirani informatički alati, formati zapisa i postupaka prenošenja podataka i informacija te interoperabilnost na tehničkoj (norme i standardi za povezivanje računalnih sustava i servisa), semantičkoj (značenje podataka) i procesnoj razini (određivanje ciljeva, modeliranje procesa i ostvarivanje suradnje između obveznika), primjenom domaćih posebnih propisa i međunarodnih tehničkih normi.

(2) Pristup modulima iz članka 5. stavka 2. ove Uredbe radi preuzimanja, unosa, povlačenja i verifikacije podataka rezerviran je za ovlaštene korisnike ISPU-a kojima se daju ovlasti za svaki modul sukladno njihovoj nadležnosti.

(3) Ovlašteni korisnici ISPU-a obvezni su podatke iz svoje nadležnosti unijeti i verificirati korištenjem za to priređenih računalnih aplikacija, sukladno ovlastima koje su im dane.

*Oblik i elektronički standard prostornog plana*

### Članak 12.

(1) Elektronički zapis grafičkog dijela elaborata prostornog plana sastoji se od:

− topološki uređenog vektorskog zapisa u gml ili shp formatu georeferenciranog u službenoj kartografskoj projekciji, strukturiranog u slojeve s pridruženim atributnim tablicama izrađenima po modelu podataka određenom posebnim propisom o sadržaju prostornih planova i

− digitalnog rasterskog zapisa i/ili zapisa u PDF formatu koji je proizveden iz zapisa iz podstavka 1. ovoga stavka.

(2) Elektronički zapis tekstualnog dijela elaborata prostornog plana obvezno sadrži digitalni tekstualni zapis odredbi za provedbu proizveden iz zapisa u atributnim tablicama u modulu ePlanovi, ako ovom Uredbom nije propisano drukčije.

(3) Iznimno od stavka 1. ovoga članka, prilikom izrade prostornog plana u skladu s pravnim pravilima Pravilnika o sadržaju, mjerilima kartografskih prikaza, obveznim prostornim pokazateljima i standardu elaborata prostornih planova (»Narodne novine«, br. 106/98, 39/04, 45/04 – ispravak i 163/04), vektorski zapis grafičkog dijela tog prostornog plana iz stavka 1. podstavka 1. ovoga članka može biti i u drugom formatu primjerenom za izradu prostornih planova, ali mora biti topološki uređen i georeferenciran u službenoj kartografskoj projekciji. Tekstualni dio takvog plana proizvodi se u PDF formatu iz elektroničkog zapisa izrađenog u programu za obradu teksta.

(4) Analognim ispisom prostornog plana smatra se ispis izrađen putem modula ePlanovi, osim za planove iz stavka 3. ovoga članka.

(5) Stavci 1., 2., 3. i 4. ovoga članka na odgovarajući se način primjenjuju i na izradu pročišćenog teksta odredbi za provedbu prostornog plana i grafičkog dijela prostornog plana u elektroničkom obliku.

*Unos elektroničkog zapisa prostornog plana u ISPU*

### Članak 13.

(1) Elektronički zapis grafičkog dijela elaborata prostornog plana iz članka 12. stavka 1. podstavka 1. ove Uredbe unosi se u ISPU putem modula ePlanovi.

(2) Elektronički zapis grafičkog dijela elaborata prostornog plana iz članka 12. stavka 1. podstavka 2. ove Uredbe i tekstualnog dijela iz članka 12. stavka 2. ove Uredbe, unosi se u ISPU putem modula eKatalog unošenjem adrese izvora koja u naravi predstavlja mrežnu adresu na mrežnoj stranici županije, zavoda za prostorno uređenje županije, odnosno Grada Zagreba ili zavoda za prostorno uređenje velikog grada (u daljnjem tekstu: zavod) ili jedinice lokalne samouprave ili umetanjem privitaka uz odgovarajući set metapodataka.

(3) Elektronički zapis grafičkog dijela elaborata prostornog plana iz članka 12. stavka 1. podstavka 2. ove Uredbe može se učiniti dostupnim i putem internetskih servisa za razmjenu podataka.

## DIO TREĆI — VOĐENJE I UPRAVLJANJE INFORMACIJSKOG SUSTAVA PROSTORNOG UREĐENJA

*Subjekti ISPU-a*

### Članak 14.

(1) Subjekti ISPU-a su:

− Ministarstvo graditeljstva i prostornoga uređenja (u daljnjem tekstu: Ministarstvo)

− Hrvatski zavod za prostorni razvoj

− zavod

− stručna upravna tijela županije i jedinice lokalne samouprave, nadležna za obavljanje stručnih poslova prostornog uređenja (u daljnjem tekstu: stručno upravno tijelo)

− upravna tijela županije, Grada Zagreba i velikog grada, nadležna za obavljanje upravnih poslova prostornog uređenja i graditeljstva (u daljnjem tekstu: upravno tijelo)

− upravna tijela velikog grada, Grada Zagreba i županije, nadležna za obavljanje stručnih i tehničkih poslova procjene vrijednosti nekretnina (u daljnjem tekstu: upravno tijelo za procjenu vrijednosti nekretnina)

− Ministarstvo financija, Porezna uprava

− stručni izrađivači i

− javnopravna tijela određena posebnim propisima koja davanjem zahtjeva i mišljenja u postupku izrade i donošenja prostornih planova i/ili utvrđivanjem posebnih uvjeta, odnosno potvrđivanjem idejnog projekta sudjeluju u sustavu prostornog uređenja (u daljnjem tekstu: javnopravno tijelo određeno posebnim propisom).

(2) Subjekti ISPU-a osiguravaju nesmetan tijek i pristup podacima i informacijama i odgovorni su za ažurnost, točnost i vjerodostojnost podataka i informacija prema svojoj nadležnosti.

*Ovlašteni korisnici ISPU-a*

### Članak 15.

(1) Ovlašteni korisnici ISPU-a su zaposlenici subjekata ISPU-a koji imaju ovlasti za preuzimanje, unos, povlačenje i/ili verifikaciju podataka u modulima iz članka 5. stavka 2. ove Uredbe.

(2) Ovlasti iz stavka 1. ovoga članka, ovisno o djelokrugu rada ovlaštenika po pisanom zahtjevu subjekta ISPU-a daje Ministarstvo, ako ovom Uredbom nije propisano drukčije.

(3) Ovlasti iz stavka 1. ovoga članka za module eKatalog i ePlanovi, osim ovlasti službenicima Ministarstva i Hrvatskog zavoda za prostorni razvoj, ovisno o djelokrugu rada ovlaštenika po pisanom zahtjevu subjekta ISPU-a, daje Hrvatski zavod za prostorni razvoj.

*Ministarstvo*

### Članak 16.

(1) Ministarstvo uspostavlja, razvija i vodi ISPU te njime upravlja u suradnji s Hrvatskim zavodom za prostorni razvoj i zavodom.

(2) Ministarstvo u vođenju i upravljanju ISPU-om obavlja sljedeće poslove:

− unosi, održava i verificira podatke u modulima eDozvola, eArhiv, eInspekcija i eNekretnine

− održava zajedničke šifrarnike za module eDozvola, eArhiv, eInspekcija i eNekretnine

− administrira korisničke račune za module eDozvola, eArhiv, eInspekcija i eNekretnine

− daje objašnjenja za vođenje i upravljanje ISPU-om drugim subjektima ISPU-a i za korištenje ovlaštenim korisnicima i

− obavlja stručne i administrativno-tehničke poslova za potrebe visokog procjeniteljskog povjerenstva prema posebnom propisu.

*Hrvatski zavod za prostorni razvoj*

### Članak 17.

(1) Hrvatski zavod za prostorni razvoj u vođenju i upravljanju ISPU-om obavlja sljedeće poslove:

− unosi, održava i verificira prostorno-planske podatke i metapodatke o prostornim planovima državne razine u modulima ePlanovi i eKatalog

− određuje razinu dostupnosti podacima i informacijama u sustavu

− održava zajedničke šifrarnike za module eKatalog i ePlanovi

− administrira korisničke račune za module eKatalog i ePlanovi

− koordinira rad subjekata ISPU-a i

− daje objašnjenja za korištenje ovlaštenim korisnicima ISPU-a za module ePlanovi i eKatalog.

(2) Ako je Hrvatski zavod za prostorni razvoj stručni izrađivač prostornog plana, na njega se na odgovarajući način primjenjuju i odredbe članka 22. ove Uredbe.

(3) Ako je Hrvatski zavod za prostorni razvoj koordinator izrade prostornog plana, na njega se na odgovarajući način primjenjuju i odredbe članka 19. ove Uredbe.

*Zavod*

### Članak 18.

(1) Zavod u vođenju i upravljanju ISPU-om obavlja sljedeće poslove:

− unosi, održava i verificira prostorno-planske podatke i metapodatke o prostornim planovima područne (regionalne) razine u modulima ePlanovi i eKatalog − unosi, održava i verificira metapodatke o prostornim planovima lokalne razine u modulu eKatalog

− kontinuirano prati stanje u prostoru i daje preporuke Hrvatskom zavodu za prostorni razvoj za daljnji razvoj ISPU-a

− kontinuirano prati sve podatke na svojem području koje u modul ePlanovi unosi stručno upravno tijelo i/ili stručni izrađivači

− vodi računa o ažurnosti unosa podataka

− daje objašnjenja ovlaštenim korisnicima ISPU-a u cilju poboljšanja kvalitete i ažurnosti podataka i

− izrađuje i unosi u modul ePlanovi u vektorskom obliku obuhvat prostornog plana lokalne razine za koji je donesena odluka o izradi na zahtjev stručnog upravnog tijela.

(2) Ako je zavod stručni izrađivač prostornog plana, na njega se na odgovarajući način primjenjuju i odredbe članka 22. ove Uredbe.

(3) Ako je zavod koordinator izrade prostornog plana, na njega se na odgovarajući način primjenjuju i odredbe članka 19. ove Uredbe.

*Stručno upravno tijelo*

### Članak 19.

(1) Stručno upravno tijelo može preuzimati podatke iz ISPU-a za svoje područje i obavljati druge poslove u skladu s ovom Uredbom.

(2) Stručno upravno tijelo obvezno je:

− dostaviti Hrvatskom zavodu za prostorni razvoj i nadležnom zavodu odluku o izradi prostornog plana u elektronskom obliku

− učitati u ISPU putem modula ePlanovi granicu obuhvata prostornog plana u gml ili shp formatu ili zatražiti od nadležnog zavoda da to učini u roku od petnaest dana od dana objave odluke o izradi prostornog plana

− unijeti putem modula ePlanovi metapodatke o tijeku izrade i donošenja prostornog plana, počevši s unosom najkasnije u roku od 7 dana od dana objave odluke o izradi prostornog plana

− dostaviti nadležnom zavodu obavijest o javnoj raspravi najkasnije petnaest dana prije početka javne rasprave

− dostaviti nadležnom zavodu odluku o donošenju prostornog plana, u roku petnaest dana od dana objave odluke o donošenju prostornog plana.

*Upravno tijelo*

### Članak 20.

Upravno tijelo može preuzimati podatke iz ISPU-a za svoje područje i obavljati druge poslove u skladu s ovom Uredbom.

*Upravno tijelo za procjenu vrijednosti nekretnina*

### Članak 21.

Upravno tijelo za procjenu vrijednosti nekretnina može preuzimati podatke iz ISPU-a za svoje područje i obavljati druge poslove u skladu s ovom Uredbom.

*Stručni izrađivač*

### Članak 22.

(1) Stručni izrađivač može u svrhu izrade prostornog plana bez naknade preuzimati podatke iz ISPU-a i elektroničke zapise iz članka 12. stavka 3. ove Uredbe od zavoda, nositelja izrade prostornog plana i drugih stručnih izrađivača prostornih planova.

(2) Stručni izrađivač obvezan je:

− nositelju izrade dostaviti elaborat nacrta prijedloga prostornog plana i prijedlog plana za javni uvid u analognom i elektroničkom obliku iz članka 12. ove Uredbe u rokovima određenom ugovorom o izradi prostornog plana

− učitati putem modula ePlanovi nacrt prijedloga prostornog plana i nacrt konačnog prijedloga prostornog plana u gml ili shp formatu

− učitati putem modula ePlanovi prijedlog prostornog plana za javnu raspravu i konačni prijedlog prostornog plana u gml ili shp formatu

− učitati putem modula ePlanovi prostorni plan u gml ili shp formatu najkasnije u roku od 8 dana od dana objave odluke o donošenju prostornog plana

− dostaviti nositelju izrade prostornog plana i nadležnom zavodu elaborat prostornog plana u analognom i elektronskom obliku iz članka 12. ove Uredbe u roku od petnaest dana od dana objave odluke o donošenju prostornog plana

− dostaviti bez naknade nadležnom zavodu elaborat prostornog plana u analognom i elektronskom obliku iz članka 12. stavka 3. ove Uredbe u roku od trideset dana od dana dostave pisanog zahtjeva zavoda.

(3) Nacrt prijedloga prostornog plana i nacrt konačnog prijedloga prostornog plana koji su učitani putem modula ePlanovi dostupni su za pregled samo ovlaštenim korisnicima modula ePlanovi te se ne objavljuju u javnom dijelu ISPU-a.

*Ispravak greške stručnog izrađivača*

### Članak 23.

(1) Ako prilikom unosa u modul ePlanovi elektronički oblik prijedloga prostornog plana ne prođe formalnu računalnu kontrolu ispravnosti ugrađenu u modul ePlanovi i/ili se gml, odnosno shp datoteke ne prikažu u ISPU na ispravan način, stručni izrađivač obvezan je bez naknade ispraviti greške i osigurati ispravan prikaz najkasnije u roku od 3 radna dana prije početka javne rasprave.

(2) Ako prilikom unosa u modul ePlanovi elektronički oblik prostornog plana ne prođe formalnu računalnu kontrolu ispravnosti ugrađenu u modulu ePlanovi i/ili se gml, odnosno shp datoteke ne prikažu u modulu ePlanovi na ispravan način, stručni izrađivač obvezan je bez naknade ispraviti greške i osigurati ispravan prikaz najkasnije u roku od petnaest dana od dana objave odluke o donošenju prostornog plana.

(3) Ako zavod utvrdi da prostorni plan iz članka 12. stavka 3. ove Uredbe nije topološki uređen i georeferenciran na odgovarajući način, stručni izrađivač obvezan je bez naknade ispraviti greške i dostaviti zavodu uređeni plan najkasnije u roku od trideset dana od dana dostave pisanog zahtjeva zavoda.

*Dostava podataka*

### Članak 24.

Dostava podataka u elektroničkom obliku prema ovoj Uredbi ne isključuje obvezu dostave analognih podataka propisanu drugim propisom.

*Izjava o sukladnosti*

### Članak 25.

(1) Uz analogni i elektronički zapis prostornog plana, odnosno drugog dokumenta nositelj izrade prostornog plana dostavlja izjavu o sukladnosti elektroničkog i analognog zapisa prostornog plana, odnosno drugog dokumenata.

(2) Izjavu o sukladnosti iz stavka 1. ovoga članka potpisuje ovlaštena osoba nositelja izrade prostornog plana i odgovorni voditelj izrade nacrta prijedloga prostornog plana.

*Dostava prostornih planova izrađenih u skladu s pravnim pravilima Pravilnika o sadržaju, mjerilima kartografskih prikaza, obveznim prostornim pokazateljima i standardu elaborata prostornih planova*

### Članak 26.

(1) Nositelj izrade prostornog plana izrađenog u skladu s pravnim pravilima Pravilnika o sadržaju, mjerilima kartografskih prikaza, obveznim prostornim pokazateljima i standardu elaborata prostornih planova, a koji je plan donesen nakon stupanja na snagu ove Uredbe, obvezan je dostaviti mjesno nadležnom zavodu elektronički zapis tog plana, u roku od petnaest dana od dana objave odluke o njegovom donošenju.

(2) Nositelj izrade izmjena i/ili dopuna prostornog plana izrađenih u skladu s pravnim pravilima Pravilnika o sadržaju, mjerilima kartografskih prikaza, obveznim prostornim pokazateljima i standardu elaborata prostornih planova koje su donesene nakon stupanja na snagu ove Uredbe, obvezan je dostaviti mjesno nadležnom zavodu elektronički zapis pročišćenog teksta odredbi za provedbu prostornog plana objavljenog nakon stupanja na snagu ove Uredbe i pripadajući grafički dio prostornog plana u elektroničkom obliku u roku od petnaest dana od dana objave pročišćenog teksta.

(3) Vektorski zapis grafičkih dijelova prostornog plana iz stavaka 1. i 2. ovoga članka stručni izrađivač je obvezan nositelju izrade na njegov zahtjev dostaviti uređen u skladu člankom 12. stavkom 3. ove Uredbe, bez naknade.

*Dostava dijelova prostornih planova izrađenih u skladu s pravnim pravilima Pravilnika o sadržaju, mjerilima kartografskih prikaza, obveznim prostornim pokazateljima i standardu elaborata prostornih planova*

### Članak 27.

(1) Zavodi su obvezni dostaviti Hrvatskom zavod za prostorni razvoj elektroničke zapise karata l, 2 i 3 prostornih planova područja posebnih obilježja, prostornih planova županije i prostornih planova uređenja grada ili općine izrađenih u skladu s pravnim pravilima Pravilnika o sadržaju, mjerilima kartografskih prikaza, obveznim prostornim pokazateljima i standardu elaborata prostornih planova, koje su važeće na dan stupanja na snagu ove Uredbe na digitalnom mediju u GeoTlFF formatu, georeferencirane u službenoj kartografskoj projekciji točnosti jednake izvornicima podloga na kojim su izrađeni grafički dijelovi planova i obrezane po granicama obuhvata, a tumače planskog znakovlja i obrasce za ovjeru prostornih planova u PDF, TIFF ili JPEG formatu.

(2) Ako zavod nije u mogućnosti iz dostupnih mu izvora proizvesti odgovarajuće GeoTlFF-ove, nositelji izrade prostornog plana ili stručni izrađivač obvezan je dostaviti zavodu na njegov zahtjev vektorski zapis grafičkog dijela prostornog plana uređen u skladu s člankom 12. stavkom 3. ove Uredbe iz kojeg se isti može proizvesti, bez naknade u roku od petnaest dana od dana primitka zahtjeva.

(3) Uz elektroničke zapise iz stavka 1. ovoga članka dostavljaju se i tablice kojima se definira veza pojedinog kartografskog prikaza s temama standardiziranim u ISPU-u i koje su sastavni dio pravilnika kojim se propisuje sadržaj prostornih planova.

(4) Zapisi iz stavka 1. ovoga članka mogu se dostaviti i putem internetskih servisa za razmjenu podataka.

*Objava prostornih planova izrađenih u skladu s pravnim pravilima Pravilnika o sadržaju, mjerilima kartografskih prikaza, obveznim prostornim pokazateljima i standardu elaborata prostornih planova*

### Članak 28.

(1) Zavodi su obvezni sve datoteke zapisa prostornih planova iz članka 12. stavka 1. podstavka 2. ove Uredbe koji su im dostavljeni sukladno članku 26. stavcima 1. i 2. ove Uredbe objaviti putem modula eKatalog kao priloge uz pripadajući set metapodataka u roku od 5 dana od dana njihova primitka.

(2) Zapise iz stavka 1. ovoga članka zavod može objaviti putem modula eKatalog i unošenjem jedne ili više adresa izvora koje u naravi predstavljaju adrese mrežnih stranica na mrežnoj stranici županije, zavoda ili jedinice lokalne samouprave, ako se na njima nalaze svi dijelovi elaborata plana

(3) U slučaju promjene adrese mrežne stranice iz stavka 2. ovoga članka, nositelj izrade prostornog plana obvezan je dostaviti zavodu novu adresu.

*Objava prijedloga prostornih planova za javnu raspravu koji se izrađuju u skladu s pravnim pravilima Pravilnika o sadržaju, mjerilima kartografskih prikaza, obveznim prostornim pokazateljima i standardu elaborata prostornih planova*

### Članak 29.

(1) Nositelj izrade izmjena i/ili dopuna prijedloga prostornog plana za javnu raspravu koje se izrađuju u skladu s pravnim pravilima Pravilnika o sadržaju, mjerilima kartografskih prikaza, obveznim prostornim pokazateljima i standardu elaborata prostornih planova obvezan je objaviti na svojim mrežnim stranicama elektronički zapis tog prijedloga najkasnije jedan dan prije dana početka javne rasprave.

(2) Ako nositelj izrade iz stavka 1. ovoga članka nema mrežne stranice, obvezan je elektronički zapis prijedloga izmjena i/ili dopuna prijedloga prostornog plana za javnu raspravu dostaviti Ministarstvu radi objave na njegovim mrežnim stranicama.

(3) Grafički dijelovi prijedloga prostornog plana iz stavka 1. ovoga članka objavljuju se u PDF formatu ili drugom formatu za koji postoji preglednik besplatno dostupan javnosti.

## DIO ČETVRTI — PRIJELAZNA I ZAVRŠNA ODREDBA

*Uspostava internetskih servisa za razmjenu podataka*

### Članak 30.

(1) Javnopravna tijela određena posebnim propisima su dužna uspostaviti internetske servise za razmjenu podataka iz članka 6. ove Uredbe u roku propisanom posebnim propisom kojim se uređuje NIPP.

(2) Do uspostave internetskih servisa iz stavka 1. ovoga članka javnopravna tijela određena posebnim propisima dužna su u roku od petnaest dana od dana primitka zahtjeva drugim subjektima ISPU-a dostavljati podatke iz svoje nadležnosti u elektronskom obliku na digitalnim medijima ili na drugi prihvatljiv način.

(3) Podaci iz stavka 2. ovoga članka dostavljaju se u GeoTIFF, shp, gml formatu ili drugom formatu prihvatljivom subjektu ISPU-a, georeferenciranom u službenoj kartografskoj projekciji s naznakom datuma zadnjeg ažuriranja podataka i opisanim metapodacima u skladu s posebnim propisima.

(4) Za dostavu podataka iz stavaka 2. i 3. ovoga članka javnopravna tijela određena posebnim propisima ne mogu tražiti naknadu.

### Članak 31.

Ova Uredba stupa na snagu osmoga dana od dana objave u »Narodnim novinama«.

Klasa: 022-03/15-03/103

Urbroj: 50301-05/05-15-2

Zagreb, 22. listopada 2015.

Predsjednik  
Zoran Milanović, v. r.
