import csv
import glob
import psycopg2


# read original csv, manipuulate values, return values as list, write new csv file,
# push to postgresql db

def hasprodai(file_path):
    shortened_file = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter='$')
        next(reader)
        i = 0
        for row in reader:
            i += 1
            row[5] = row[5].replace('.', '')
            row[5] = row[5].replace('/', ' ')
            row[5] = row[5].replace("\\", " ")
            if row[5] == 'NA' or row[5] == 'N/A' or row[5] == '' or len(row[5]) == 0:
                pass   
            else:
                shortened_file.append([row[0],row[5]])    
    return shortened_file 

def noprodai(file_path):
    none_list = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter='$')
        next(reader)
        i = 0
        for row in reader:
            i += 1
            row[5] = row[5].replace('.', '')
            row[5] = row[5].replace('/', ' ')
            row[5] = row[5].replace("\\", " ")
            if row[5] == 'NA' or row[5] == 'N/A' or row[5] == '' or len(row[5]) == 0:
                none_list.append([row[0],row[5]])
            else:
                pass
    return none_list

def mapper(newcsv, shortened_file):
    notmapped = []
    with open(newcsv, 'w', newline='') as out:
        writer = csv.writer(out, delimiter='$')
        writer.writerow(['primaryid', 'prodai', 'classid', 'classname', 'indication'])
        for ls in shortened_file:
    
            x = ls[0]
            y = ls[1]
            if y.endswith('HYDROCHLORIDE') or y.endswith('CHLORIDE') or y.endswith('OXIDE'):
                notmapped.append(y)
            elif y.endswith('COSMETICS'):
                writer.writerow([x,y,1,'cosmetic','non-prescription use'])
            elif y.endswith('MAB') or y.startswith('GALCANEZUMAB-GNLM') or y.startswith('EMGALITY')or y.startswith('COSENTYX') or y.startswith('DUPIXENT') or y.endswith('DUPIXENT') or y.startswith('XOLAIR') or y.startswith('ACTEMRA') or y.startswith('STELARA'):
                writer.writerow([x,y,2,'monoclonal antibody','autoimmune diseases'])       
            elif y.startswith('ADAPALENE'):
                writer.writerow([x,y,3,'retinoid', 'acne vulgaris'])       
            elif y.startswith(('PREDNIS','METHYLPREDNIS'),0,20) or y.endswith(('LONE','SONE'),0,20) or y.startswith('MOMETASONE FUROATE') or y.startswith('FLUTICASONE PROPIONATE') or y.startswith('FLONASE'):
                writer.writerow([x,y,4,'corticosteroid', 'immunosupressant'])
            elif y.startswith('ACETAMINOPHEN') or y.startswith('TYLENOL'):
                writer.writerow([x,y,5,'analgesic', 'fever reducer'])
            elif y.startswith('ASPIRIN') or y.startswith('IBUPROFEN') or y.startswith('MELOXICAM') or y.startswith('MOBIC') or y.endswith('FENAC') or y.endswith('PROFEN') or y.startswith('CELECOXIB') or y.startswith('CELEBREX') or y.startswith('NAPROXEN') or y.startswith('NAPROSYN'):
                writer.writerow([x,y,6,'nonsteroidal anti-inflammatory drug', 'fever reducer/inflammation/pain management'])
            elif y.endswith('STATIN', 0, 12) or y.endswith('STATIN'):
                writer.writerow([x,y,7,'HMG-CoA reductase inhibitor', 'hyperlipidemia'])
            elif y.endswith('IDE'):
                if len(y) < 20:
                    writer.writerow([x,y,8,'diuretic', 'hypertension'])
            elif y.startswith('METHOTREXATE') or y.startswith('CYTARABINE') or y.startswith('FLUDARABINE PHOSPHATE') or y.startswith('FLUDARA'):
                writer.writerow([x,y,9,'antimetabolites', 'cancer treatment'])
            elif y.startswith('AVONEX') or y.startswith('INTERFERON BETA-1A'):
                writer.writerow([x,y,10,'interferon', 'multiple sclerosis'])
            elif y.startswith('GABAPENTIN') or y.startswith('LYRICA') or y.startswith('PREGABALIN') or y.startswith('BACLOFEN'):
                writer.writerow([x,y,11,'GABA analogue', 'anticonvulsant/fibromyalgia/nerve pain'])
            elif y.startswith(('METFORMIN','METFORMIN HYDROCLORIDE')):
                writer.writerow([x,y,12,'biguanides', 'diabetic management'])
            elif y.startswith('AMLODIPINE'):
                writer.writerow([x,y,13,'calcium channel blocker', 'hypertension/chest pain'])
            elif y.startswith('INFLECTRA') or y.startswith('INFLIXIMAB-DYYB') or y.startswith('HUMIRA') or y.startswith('REMICADE') or y.endswith('INFLIXIMAB') or y.startswith('CERTOLIZUMAB PEGOL') or y.startswith('CIMZIA'):
                writer.writerow([x,y,14,'TNF blocking agent', 'autoimmune diseases'])
            elif y.startswith('XARELTO') or y.startswith('WARFARIN') or y.startswith('RIVAROXABAN') or y.startswith('DABIGATRAN ETEXILATE MESYLATE'):
                writer.writerow([x,y,15,'anticoagulant', 'blood clots'])
            elif y.startswith('ENBREL') or y.startswith('ETANERCEPT'):
                writer.writerow([x,y,16,'TNF inhibitor', 'autoimmune diseases'])
            elif y.startswith('ELIQUIS') or y.startswith('APIXABAN'):
                writer.writerow([x,y,17,'factor xa inhibitor anticoagulant', 'nonvalvular atrial fibrilation'])
            elif y.startswith('OTEZLA') or y.startswith('APREMILAST') or y.startswith('SILDENAFIL CITRATE'):
                writer.writerow([x,y,18,'phosphodiesterase inhibitor', 'autoimmune diseases/erectile dysfunction'])
            elif y.startswith('PROAIR HFA') or y.startswith('ALBUTEROL SULFATE'):    
                writer.writerow([x,y,19,'beta-2 adrenergic agonist', 'asthma'])
            elif y.startswith('SYNTHROID') or y.startswith('LEVOTHYROXINE') or y.startswith('TESTOSTERONE') or y.startswith('ESTROGENS CONJUGATED') or y.startswith('ETONOGESTREL') or y.startswith('NEXPLANON') or y.startswith('IMPLANON') or y.startswith('MELATONIN') or y.startswith('ESTRADIOL') or y.startswith('ESTRACE') or y.endswith('TROPIN') or y.startswith('LEVONORGESTREL') or y.startswith('TESTOSTERONE CYPIONATE') or y.startswith('DEPO-TESTOSTERONE'): 
                writer.writerow([x,y,20,'hormone', 'hormone deficiency'])
            elif y.endswith('PRIL'):    
                writer.writerow([x,y,21,'ACE_inhibitor', 'hypertenstion'])
            elif y.startswith('ORENCIA') or y.startswith('ABATACEPT') or y.startswith('GLATIRAMER ACETATE') or y.startswith('REVLIMID') or y.startswith('LENALIDOMIDE'):
                writer.writerow([x,y,22,'immunomodulator', 'autoimmune diseases'])
            elif y.startswith('PACLITAXEL') or y.startswith('TAXOL') or y.startswith('VINCRISTINE SULFATE') or y.startswith('DOCETAyEL') or y.startswith('TAXOTERE'):  
                writer.writerow([x,y,23,'antimicrotubule agent', 'cancer treatment'])
            elif y.startswith('PROGRAF') or y.startswith('TACROLIMUS'):
                writer.writerow([x,y,24,'immunosuppressant', 'prophylayis of organ rejection'])
            elif y.startswith('SINEMET') or y.startswith('CARBIDOPA\LEVODOPA') or y.startswith('LEVODOPA'):    
                writer.writerow([x,y,25,'decarboyylase inhibitor/CNS agent', 'parkinsons disease'])
            elif y.startswith('LANTUS') or y.startswith('INSULIN GLARGINE') or y.startswith('INSULIN NOS') or y.startswith('INSULIN ASPART') or y.startswith('NOVOLOG')or y.startswith('INSULIN HUMAN') or y.startswith('MYXREDLIN') or y.startswith('HUMALOG') or y.startswith('INSULIN LISPRO'):  
                writer.writerow([x,y,26,'human insulin analog', 'glycemic management/T1 diabetes/T2 diabetes'])
            elif y.endswith('AZEPAM') or y.endswith('ZOLAM'):
                writer.writerow([x,y,27,'benzodiazepine', 'anxiety'])
            elif y.endswith('IUM') or y.endswith('URONIUM'):        
                writer.writerow([x,y,28,'nondepolarizing paralytics', 'anesthesia'])
            elif y.startswith('XELJANZ') or y.startswith('TOFACITINIB') or y.startswith('IMATINIB MESYLATE') or y.startswith('EVEROLIMUS') or y.endswith('LIB') or y.endswith('NIB') or y.endswith('TINIB') or y.startswith('ANIB') or y.endswith('RAFENIB') or y.startswith('IBRANCE') or y.startswith('PALBOCICLIB'):
                writer.writerow([x,y,29,'tyrosine kinase inhibitor', 'autoimmune diseases/cancer treatment'])
            elif y.startswith('VITAMIN') or y.startswith('BIOTIN') or y.startswith('UBIDECARENONE') or y.startswith('MINERALS\VITAMINS') or y.startswith('FERROUS SULFATE') or y.startswith('FISH OIL') or y.startswith('IRON') or y.startswith('ERGOCALCIFEROL') or y.startswith('CHOLECALCIFEROL') or y.startswith('CYANOCOBALAMIN') or y.startswith('ASCORBIC ACID') or y.startswith('FOLIC'):  
                writer.writerow([x,y,30,'vitamin/mineral/antioxidant', 'dietary supplement'])
            elif y.startswith('CLOZARIL') or y.startswith('CLOZAPINE') or y.startswith('HALOPERIDOL') or y.startswith('PALIPERIDONE PALMITATE') or y.startswith('INVEGA SUSTENNA') or y.startswith('RISPERIDONE') or y.startswith('RISPERDAL') or y.startswith('PIMAVANSERIN TARTRATE') or y.startswith('NUPLAZID') or y.startswith('QUETIAPINE') or y.startswith('OLANZAPINE') or y.startswith('ZYPREXA'):
                writer.writerow([x,y,31,'antipsychotic', 'schizophrenia'])
            elif y.endswith('AFIL'): 
                writer.writerow([x,y,32,'phosphodiesterase inhibitor', 'erectile dysfunction/hypertension'])
            elif y.endswith('ANE'):
                writer.writerow([x,y,33,'inhaled anestetics', 'anesthesia'])
            elif y.endswith('ARTAN'):
                writer.writerow([x,y,34,'angiotension receptor blocker', 'hypertension'])
            elif y.endswith('AZINE'):
                writer.writerow([x,y,35,'phenothiazines', 'antipsychotic'])   
            elif y.endswith('TIDINE') or y.endswith('ZANTAC') or y.startswith('KETOTIFEN FUMARATE') or y.endswith('ZYRTEC') or y.startswith('CETERIZINE') or y.endswith('ZINE') or y.endswith('DINE') or y.endswith('MINE') or y.startswith('DIPHENHYDRAMINE') or y.startswith('BENADRYL') or y.startswith('LORATADINE') or y.startswith('CLARITIN'):
                writer.writerow([x,y,36,'antihistamine', 'allergy'])
            elif y.endswith('BARBITAL'):
                writer.writerow([x,y,37,'barbituates', 'anxiety'])
            elif y.endswith('CAINE'):
                writer.writerow([x,y,38,'local anesthetics', 'anesthesia'])
            elif y.endswith('CILLIN'):
                writer.writerow([x,y,39,'penecillin antibiotics', 'antibiotic'])
            elif y.startswith(('TETRACYCLINE','TETRACYCLINE HYDROCHLORIDE')):
                writer.writerow([x,y,40,'tetracycline', 'antibiotic'])
            elif y.endswith('ETINE') or y.startswith('ESCITALOPRAM OXALATE') or y.startswith('LEXAPRO') or y.startswith('CITALOPRAM'):
                writer.writerow([x,y,41,'selective serotonin reuptake inhibitor', 'depression'])
            elif y.endswith('FEB') or y.endswith('FENE'):
                writer.writerow([x,y,42,'selective estrogen response modifier', 'osteoporosis/cancer treatment'])
            elif y.endswith('FLOXACIN'):
                writer.writerow([x,y,43,'fluoroquinolones', 'antibiotic'])
            elif y.endswith('FUNGIN'):
                writer.writerow([x,y,44,'echinocandin', 'antifungal'])
            elif y.endswith('GRASTIM') or y.endswith('GRAMOSTIM') or y.endswith('NEULASTA'):
                writer.writerow([x,y,45,'granulocyte colony stimulating factor', 'blood dyscrasias/febrile neutropenia'])
            elif y.endswith('IPINE') or y.startswith(('DILTIAZEM','DILTIAZEM HYDROCHLORIDE')):
                writer.writerow([x,y,46,'dihydropyridine calcium channel blocker', 'hypertension'])
            elif y.endswith('IPRAMINE'):
                writer.writerow([x,y,47,'tricyclic antidepressant', 'depression'])
            elif y.endswith('LUKAST'):
                writer.writerow([x,y,48,'LTD receptor antagonist', 'asthma'])
            elif y.endswith('NAVIR'):
                writer.writerow([x,y,49,'protease inhibitor', 'antiviral'])
            elif y.endswith('LOL') or y.startswith(('COREG','METOPROLOL SUCCINATE','METOPROLOL TARTATE')) or y.startswith('TIMOLOL MALEATE') or y.startswith('BISOPROLOL FUMARATE') or y.startswith('ZEBETA'):
                writer.writerow([x,y,50,'beta blocker', 'hypertension'])
            elif y.endswith('OXIN'):
                writer.writerow([x,y,51,'cardiac glycoside', 'arrhythmia'])
            elif y.endswith('PYHLLINE'):
                writer.writerow([x,y,52,'methlxanthine', 'bronchodialator'])
            elif y.endswith('QUINE') or y.startswith('PLAQUENIL') or y.startswith('HYDROXYCHLOROQUINE SULFATE'):
                writer.writerow([x,y,53,'quinolone derivatie','antimalarial'])
            elif y.endswith('TECAN'):
                writer.writerow([x,y,54,'topoisomerase-1 inhibitor', 'chemotherapy'])
            elif y.endswith('TOPOSIDE'):
                writer.writerow([x,y,55,'topoisomerase-2 inhibitor', 'chemotherapy'])
            elif y.endswith('TEROL') or y.startswith('FLUTICASONE FUROATE\VILANTEROL TRIFENATATE') or y.startswith('BREO'):
                writer.writerow([x,y,56,'beta-2 agonist', 'bronchodialator'])
            elif y.endswith('TINE'):
                writer.writerow([x,y,57,'allylamine antifungal', 'antifungal'])
            elif y.endswith('TRIPTAN'):
                writer.writerow([x,y,58,'5-HT1B/1D agonist', 'migrane'])
            elif y.endswith('VAPTAN'):
                writer.writerow([x,y,59,'vasopressin receptor antagonist', 'hypertension'])
            elif y.endswith('ZOSIN'):
                writer.writerow([x,y,60,'alpha-1 antagonist', 'hypertension/BPH'])      
            elif y.startswith('TRUVADA') or y.startswith('DESCOVY') or y.endswith('TENOFOVIR ALAFENAMIDE FUMARATE') or y.endswith('*DISOPROXIL FUMARATE') or y.startswith('VIREAD') or y.startswith('EMTRIVA') or y.startswith('EMTRICITABINE') or y.startswith('ATRIPLA'):
                writer.writerow([x,y,61,'reverse transcriptase inhibitor', 'antiviral'])
            elif y.startswith('TECFIDERA') or y.startswith('DIMETHYL FUMARATE'):
                writer.writerow([x,y,62,'dimethyl fumerate/fumaric acid ester', 'multiple sclerosis'])
            elif y.startswith('OXYCONTIN') or y.startswith(('OXYCODONE','OXYCODONE HYDROCHLORIDE','ACETAMINOPHEN OXYCODONE HYDROCHLORIDE','TRAMADOL HYDROCHLORIDE')) or y.startswith('CODEINE') or y.endswith('CODONE') or y.endswith('PHINE') or y.endswith('TANYL') or y.endswith('MORPHONE') or y.startswith('ROXANOL') or y.startswith('MORPHINE SULFATE') or y.startswith('SUBLIMAZE') or y.startswith('FENTANYL'):
                writer.writerow([x,y,63,'opioid agonist','pain management']) 
            elif y.startswith('TRULICITY'):
                writer.writerow([x,y,64,'glp-1 receptor agonist', 'glycemic management'])
            elif y.startswith('REMODULIN') or y.startswith('TREPROSTINIL'):
                writer.writerow([x,y,65,'prostacyclin vasodialator', 'PAH,transition from Flolan']) 
            elif y.startswith('DILANTIN') or y.startswith('PHENYTOIN') or y.startswith('VALPROIC ACID') or y.startswith('CARBAMAZEPINE') or y.startswith('TEGRETOL') or y.startswith('TOPIRAMATE') or y.startswith('TOPAMAX')or y.startswith('LEVETIRACETAM') or y.startswith('KEPPRA'):
                writer.writerow([x,y,66,'anticonvulsants','epilepsy'])
            elif y.startswith('ZITHROMAX') or y.startswith('AZITHROMYCIN') or y.startswith('BACTRIM') or y.startswith('SULFAMETHOXAZOLE\TRIMETHOPRIM'):
                writer.writerow([x,y,67,'antibacterial','bacterial infection'])
            elif y.startswith('IMIQUIMOD') or y.startswith('ALDARA'):
                writer.writerow([x,y,68,'immune response modifier','actinic keratosis/genital warts'])
            elif y.startswith('ZYLOPRIM') or y.startswith('ALOPRIM') or y.startswith('FEBUXOSTAT') or y.startswith('ALLOPURINOL'):
                writer.writerow([x,y,69,'xanthine oxidase inhibitor','gout'])
            elif y.startswith('HUMAN IMMUNOGLOBULIN G'):
                writer.writerow([x,y,70,'immune system supplement','immunodeficiency/Kawasaki syndrome/GvH disease'])
            elif y.startswith('XALATAN') or y.startswith('LATANOPROST') or y.startswith('TRAVOPROST') or y.startswith('TRAVATAN'):
                writer.writerow([x,y,71,'prostanoid selective FP receptor agonist','open-angle glaucoma/ocular hypertension'])
            elif y.startswith('ACYCLOVIR') or y.startswith('ZOVIRAX'):
                writer.writerow([x,y,72,'synthetic nucleoside analogue', 'herpes'])
            elif y.startswith('PLAVIX') or y.startswith('CLOPIDOGREL'):
                writer.writerow([x,y,73,'P2Y-12 platelet inhibitor', 'myocardial infarction/stroke/extablished peripheral arterial disease'])
            elif y.startswith('ZOFRAN') or y.startswith(('ONDANSETRON','ONDANSETRON HYDROCHLORIDE')):
                writer.writerow([x,y,74,'5-HT receptor antagonist', 'nausea prevention'])
            elif y.startswith('UPTRAVI') or y.startswith('SELEXIPAG'):
                writer.writerow([x,y,75,'prostacyclin receptor agonist', 'pulmonary arterial hypertension'])
            elif y.startswith('XYREM') or y.startswith('SODIUM OXYBATE'):
                writer.writerow([x,y,76,'CNS depressant', 'cataplexy/excessive daytime sleepiness'])
            elif y.startswith('MYCOPHENOLATE MOFETIL') or y.startswith('CELLCEPT') or y.startswith('AZATHIOPRINE') or y.startswith('IMURAN'): 
                writer.writerow([x,y,77,'antimetabolite immunosuppressant', 'prophylaxis of organ rejection'])
            elif y.startswith('OCTREOTIDE ACETATE') or y.startswith('SANDOSTATIN'): 
                writer.writerow([x,y,78, 'somatostatin analogue', 'acromegaly/diarrhea'])
            elif y.startswith('CARBOPLATIN') or y.startswith('PARAPLATIN') or y.startswith('SODIUM BICARBONATE') or y.startswith('CISPLATIN') or y.startswith('ELOXATIN') or y.startswith('OXALIPLATIN'): 
                writer.writerow([x,y,79,'alkylating agent', 'cancer treatment'])
            elif y.startswith('CYCLOSPORINE') or y.startswith('SANDIMMUNE'): 
                writer.writerow([x,y,80,'nonribosomal peptide','prophylaxis of organ rejection'])
            elif y.startswith('SPIRONOLACTONE') or y.startswith('ALDACTONE'): 
                writer.writerow([x,y,81,'aldonsterone antagonist','heart failure/edema management/hypertension'])
            elif y.startswith('MACITENTAN') or y.startswith('OPSUMIT') or y.startswith('BOSENTAN') or y.startswith('AMBRISENTAN') or y.startswith('LETAIRIS'): 
                writer.writerow([x,y,82,'endothelin receptor antagonist','PAH'])
            elif y.startswith('VENETOCLAX') or y.startswith('VENCLEXTA'): 
                writer.writerow([x,y,83,'BCL-2 inhibitor', 'cancer treatment'])
            elif y.startswith('FLUTICASONE PROPIONATE\SALMETEROL XINAFOATE') or y.startswith('ADVAIR DISKUS') or y.startswith('BUDESONIDE\FORMOTEROL FUMARATE DIHYDRATE') or y.startswith('SYMBICORT'): 
                writer.writerow([x,y,84,'corticosteroid/long-acting beta agonist', 'asthma'])
            elif y.startswith('ZOLPIDEM') or y.startswith('AMBIEN') or y.startswith('ZOPICLONE'): 
                writer.writerow([x,y,85,'sedative-hypnotic', 'insomnia'])
            elif y.startswith('LAMOTRIGINE'): 
                writer.writerow([x,y,86,'phenyltriazine', 'epilepsy/bipolar disorder'])
            elif y.startswith('LEUPROLIDE ACETATE') or y.startswith('LUPRON DEPOT'): 
                writer.writerow([x,y,87,'gonadotropin-releasing hormone agonist', 'cancer treament'])
            elif y.startswith('BORTEZOMIB') or y.startswith('VELCADE'): 
                writer.writerow([x,y,88,'antineoplastic agent/proteasome inhibitor', 'cancer treatment'])
            elif y.startswith('MIRTAZAPINE') or y.startswith('REMERON'): 
                writer.writerow([x,y,89,'antidepressant','MDD/PSTD'])
            elif y.startswith('UNSPECIFIED INGREDIENT'):
                writer.writerow([x,y,90,'unknown', 'unknown'])
            elif y.startswith('FLUOROURACIL') or y.startswith('CAPECITABINE') or y.startswith('XELODA') or y.startswith('GEMCITABINE') or y.startswith('GEMZAR'):
                writer.writerow([x,y,91,'nucleoside metabolic inhibitor', 'cancer treatment'])
            elif y.startswith('EPINEPHRINE') or y.startswith('DROXIDOPA'):
                writer.writerow([x,y,92,'alpha and beta adrenergic agonist', 'septic and anaphylaxis shock'])
            elif y.startswith('ERENUMAB-AOOE') or y.startswith('AIMOVIG'):
                writer.writerow([x,y,93,'calcitonin gene-related peptide receptor antagonist', 'migraine'])
            elif y.startswith('MINOXIDIL') or y.startswith('ROGAINE') or y.startswith('NITROGLYCERIN') or y.startswith('EPOPROSTENOL') or y.startswith('FLOLAN'):
                writer.writerow([x,y,94,'vasodialator', 'blood vessel expansion'])
            elif y.startswith('BONIVA') or y.startswith('IBANDRONIC') or y.startswith('ZOLEDRONIC ACID') or y.startswith('ZOMETA'):
                writer.writerow([x,y,95,'bisphosphonate', 'osteoporosis'])
            elif y.startswith('REMDESIVIR'):
                writer.writerow([x,y,96,'SARS-CoV-2 nucleotide analog RNA polymerase inhibitor', 'antiviral'])
            elif y.startswith('BRIMONIDINE TARTRATE') or y.startswith('ALPHAGAN'):
                writer.writerow([x,y,97,'alpha adrenergic agonist', 'open-angle glaucoma/ocular hypertension'])
            elif y.startswith('NIRAPARIB') or y.startswith('ZEJULA'):
                writer.writerow([x,y,98,'PARP inhibitor','cancer treatment'])
            elif y.startswith('FEMARA') or y.startswith('LETROZOLE') or y.startswith('ANASTROZOLE'):
                writer.writerow([x,y,99,'aromatase inhibitor', 'cancer treatment'])
            elif y.startswith('BIMATOPROST') or y.startswith('LUMIGAN'):
                writer.writerow([x,y,100,'prostaglandin analog', 'open angle glaucoma/ocular hypertension'])
            elif y.startswith('FLOMAX') or y.startswith('TAMSULOSIN'):
                writer.writerow([x,y,101,'alpha-1 adrenoceptor antagonist', 'benign prostatic hyperplasia'])
            elif y.startswith('AMITRIPTYLINE'):
                writer.writerow([x,y,102,'tricyclic antidepressant', 'anxiety/PTSD'])
            elif y.startswith('MIRABEGRON') or y.startswith('MYRBETRIQ'):
                writer.writerow([x,y,103,'beta-3 adrenergic agonist', 'overactive bladder'])
            elif y.startswith('VANCOMYCIN') or y.startswith('VANCOCIN'):
                writer.writerow([x,y,104,'glycopeptide antibiotic', 'gram-positive bacterial infection'])
            elif y.startswith('CALCIUM CARBONATE'):
                writer.writerow([x,y,105,'antacid', 'heart burn'])
            elif y.startswith('DOXORUBICIN'):
                writer.writerow([x,y,106,'anthracycline', 'cancer treatment'])
            elif y.startswith('COBICISTAT\ELVITEGRAVIR\EMTRICITABINE\TENOFOVIR DISOPROXIL FUMARATE'):
                writer.writerow([x,y,107, 'HIV-1 INSTI/CYP3A inhibitor/nucleoside reverse transcriptase inhibitor','antiviral'])
            elif y.startswith('EZETIMIBE') or y.startswith('ZETIA'):
                writer.writerow([x,y,108,'lipid-lowering compound', 'hypercholesterolemia'])
            elif y.startswith('CALCIUM CHLORIDE\DEXTROSE\MAGNESIUM CHLORIDE\SODIUM CHLORIDE\SODIUM LACTATE') or y.startswith('DELFLEX'):
                writer.writerow([x,y,109, 'dialysis adjunct', 'CKF'])
            elif y.startswith('CYCLOBENZAPRINE') or y.startswith('FLEXERIL'):
                writer.writerow([x,y,110,'skeletal muscle relaxant', 'muscle spasm'])
            elif y.startswith('CEFTRIAXONE') or y.startswith('ROCEPHIN'):
                writer.writerow([x,y,111,'cephalosporin', 'antibiotic'])
            elif y.startswith('ENOXAPARIN') or y.startswith('LOVENOX'):
                writer.writerow([x,y,112,'molecular weight herapin', 'DVT'])
            elif y.startswith('EMPAGLIFLOZIN') or y.startswith('JARDIANCE'):
                writer.writerow([x,y,113,'sodium-glucose co-transporter 2', 'glucose management'])
            elif y.startswith('MEROPENEM') or y.startswith('MERREM'):
                writer.writerow([x,y,114,'penem antibacterial', 'bacterial infection'])
            elif y.startswith('AMIODARONE') or y.startswith('NEXTERONE'):
                writer.writerow([x,y,115,'postassium channel blocker', 'arrhythmia'])
            elif y.startswith('RIOCIGUAT') or y.startswith('ADEMPAS'):
                writer.writerow([x,y,116,'soluble guanylate cyclase stimulator', 'CTEPH/PAH'])
            elif y.startswith('LACTULOSE') or y.startswith('POLYETHYLENE GLYCOLS') or y.startswith('SENNOSIDES') or y.startswith('POLYETHYLENE GLYCOL 3350'):
                writer.writerow([x,y,117,'laxative', 'constipation'])
            elif y.startswith('MYCOPHENOLIC ACID') or y.startswith('MYFORTIC'):
                writer.writerow([x,y,118,'guanosine nucleotide inhibitor', 'immunosuppressant'])
            elif y.startswith('AMPHETAMINE ASPARTATE\AMPHETAMINE SULFATE\DEXTROAMPHETAMINE SACCHARATE\DEXTROAMPHETAMINE SULFATE'):
                writer.writerow([x,y,119,'stimulat','ADD/ADHD'])
            elif y.startswith('SITAGLIPTIN PHOSPHATE'):
                writer.writerow([x,y,120,'dipeptidyl peptidase-4 inhibitor', 'diabetic management'])
            elif y.startswith('VOXELOTOR'):
                writer.writerow([x,y,121,'hemoglobin S polymerization inhibitor', 'sickle cell disease'])
            elif y.startswith('CLARITHROMYCIN'):
                writer.writerow([x,y,122,'macrolide antibiotic', 'bacterial infection'])
            elif y.startswith('ANAKINRA'):
                writer.writerow([x,y,123,'interleukin antagonist', 'rheumatoid arthritis'])
            elif y.startswith('FULVESTRANT'):
                writer.writerow([x,y,124,'estrogen receptor antagonist', 'cancer treatment'])
            elif y.startswith('ELEXACAFTOR\IVACAFTOR\TEZACAFTOR'):
                writer.writerow([x,y,125,'cystic fibrosis transmembrane conductance regulator corrector/potentiator', 'cystic fibrosis'])
            elif y.startswith('CANNABIDIOL'):
                writer.writerow([x,y,126,'phytocannabinoid', 'seizures'])
            elif y.startswith('NALTREXONE'):
                writer.writerow([x,y,127,'opioid antagonist', 'alcoholism/opioid dependence'])
            elif y.startswith('PIRFENIDONE'):
                writer.writerow([x,y,128,'pyridone', 'IPF'])
            elif y.startswith('GUAIFENESIN'):
                writer.writerow([x,y,129,'expectorant', 'common cold'])
            elif y.startswith(('VENLAFAXINE','VENLAFAXINE HYDROCHLORIDE')):
                writer.writerow([x,y,130,'serotonin and norepinephrine reuptake inhibitor', 'depression'])
            elif y.startswith('BUPROPION'):
                writer.writerow([x,y,131,'norepinephrine and dopamine reuptake inhibitor', 'depression'])
            elif y.startswith('LINEZOLID'):
                writer.writerow([x,y,132,'oxazolidinone', 'antibiotic'])
            elif y.startswith('LEUCOVORIN'):
                writer.writerow([x,y,133,'folic acid analog', 'cancer treatment adjunct'])
            elif y.startswith('CEPHALEXIN'):
                writer.writerow([x,y,134,'cephlasporin antibiotic', 'respiratory tract infection'])
            elif y.startswith('OXYGEN'):
                writer.writerow([x,y,135,'medical gas', 'compromised breathing'])
            elif y.startswith('DARBEPOETIN ALFA'):
                writer.writerow([x,y,136,'erythropoiesis-stimulating agent', 'anemia'])
            elif y.startswith('PANCRELIPASE AMYLASE\PANCRELIPASE LIPASE\PANCRELIPASE PROTEASE'):
                writer.writerow([x,y,137,'amylase/lipase/protease', 'exocrine pancreatic insufficiency'])
            elif y.startswith('ABIRATERONE ACETATE'):
                writer.writerow([x,y,138,'CYP17 inhibitor', 'cancer treatment'])
            elif y.startswith('FENOFIBRATE'):
                writer.writerow([x,y,139,'peroxisome proliferator-activated receptor alpha agonist', 'hypertriglyceridemia'])
            elif y.startswith('HUMAN C1-ESTERASE INHIBITOR'):
                writer.writerow([x,y,140,'c1 esterase inhibitor', 'hereditary angiodedema'])
            elif y.startswith('ANTIHEMOPHILIC FACTOR, HUMAN RECOMBINANT'):
                writer.writerow([x,y,141,'coagulation factor', 'hemophilia A'])
            elif y.startswith('CLINDAMYCIN'):
                writer.writerow([x,y,142,'lincomycin antibiotic', 'bacterial infection'])
            elif y.startswith('COLCHICINE'):
                writer.writerow([x,y,143,'anti-gout agent', 'gout'])
            elif y.startswith(r'FLUTICASONE FUROATE\UMECLIDINIUM BROMIDE\VILANTEROL TRIFENATATE'):
                writer.writerow([x,y,144,'corticosteroid/anticholinergic/long-acting beta2-adrenergic agonist', 'COPD'])
            elif y.startswith('TICAGRELOR'):
                writer.writerow([x,y,145,'P2Y12 platelet inhibitor', 'acute coronary syndrome/myocardial infarction'])
            elif y.startswith('URSODIOL'):
                writer.writerow([x,y,146,'gallstone dissolution agent', 'gallstone prevention/primary biliary cirrhosis'])
            elif y.startswith('COBICISTAT\ELVITEGRAVIR\EMTRICITABINE\TENOFOVIR ALAFENAMIDE FUMARATE'):
                writer.writerow([x,y,147,'integrase strand transfer inhibitor/CYP3A inhibotor/nucleoside analog reverse transcriptase inhibitor', 'antiviral'])
            elif y.startswith('AMIKACIN'):
                writer.writerow([x,y,148,'aminoglycoside antibiotic', 'antibacterial'])
            elif y.startswith('OLAPARIB'):
                writer.writerow([x,y,149,'poly (ADP-ribose) polymerase inhibitor', 'cancer treatment'])
            elif y.startswith(('ESOMEPRA','PANTOPRA','OMEPRA','LANSOPRA'),0,10):
                writer.writerow([x,y,150,'proton-pump inhibitor', 'GERD'])
            else:
                notmapped.append(y)
    return notmapped

def clean_reactions(reactions_filepath, newreactions_filepath):
    reactions_by_id = {}
    reactions_by_id_list = []
    with open(reactions_filepath, 'r') as csvfile, open(newreactions_filepath, 'w', newline='') as outcsvfile:
        reacreader = csv.reader(csvfile, delimiter='$')
        next(reacreader) #skip headers

        for row in reacreader:

            ptlist = reactions_by_id.get(row[0], [])
            ptlist.append(row[2])
            reactions_by_id[row[0]] = ptlist

        reactions_by_id_list.append(reactions_by_id)
        
        writer = csv.writer(outcsvfile, delimiter='$')
        for k,v in reactions_by_id_list[0].items():
            
            writer.writerow([k,v])
        print('file is located at:' + ' ' + str(newreactions_filepath))

def clean_outcomes(outcomes_filepath, newoutcomes_filepath):
    outcomes_by_id = {}
    outcomes_by_id_list = []
    with open(outcomes_filepath, 'r') as csvfile, open(newoutcomes_filepath, 'w', newline='') as outcsvfile:
        outcreader = csv.reader(csvfile, delimiter='$')
        next(outcreader) #skip headers

        for row in outcreader:
            ptlist = outcomes_by_id.get(row[0], [])
            ptlist.append(row[2])
            outcomes_by_id[row[0]] = ptlist
        outcomes_by_id_list.append(outcomes_by_id)
        
        writer = csv.writer(outcsvfile, delimiter='$')
        for k,v in outcomes_by_id_list[0].items():
            
            writer.writerow([k,v])
        print('file is located at:' + ' ' + str(newoutcomes_filepath))

def db_push(host,dbname,user,password,filepath,db_table,columns, sep):
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    cur = conn.cursor()

    for path in glob.iglob(filepath):

        with open(path, 'r') as f:
            next(f)
            cur.copy_from(f, db_table, columns=columns,sep=sep)

    conn.commit()
    conn.close()
