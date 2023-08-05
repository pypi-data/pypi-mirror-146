
import pathlib
import urllib.request
import gzip
import shutil
import tarfile
import zipfile
import os
import requests

from utranslate._managers.directory import directory_handler
from utranslate._managers.download import downloader
from utranslate._managers.extract import extractor



class my_setup:

    def __init__(self):

        self.data_types = {'GNOME_Opus':145706,
                    'KDE4_Opus':97227,
                    'Tanzil_Opus':187080,
                    'Tatoeba_Opus':4698,
                    'OpenSubs2013_Opus':4222,
                    'HindEnCorp':273885,
                    'Hindi_English_Wordnet_Linkage':175175,
                    'Mahashabdkosh_Administrative_Domain_Dictionary':66474,
                    'Mahashabdkosh_Administrative_Domain_Examples':46825,
                    'Mahashabdkosh_Administrative_Domain_Definitions':46523,
                    'TED_talks':42583,
                    'Indic_multi_parallel_corpus':10349,
                    'Judicial_domain_corpus_I'	:5007,
                    'Judicial_domain_corpus_II'	:3727,
                    'Different_Indian_Government_websites'	:123360,
                    'Wiki_Headlines'	:32863,
                    'Book_Translations_Gyaan_Nidhi_Corpus'	:227123,
                    'Different_Indian_Government_websites_2'	:69013,
                    'Different_Indian_Government_websites_3'	:47842}

        self.directory_handler = directory_handler()
        self.downloader = downloader()
        self.extractor = extractor()



    def driectory_setup(self):

        print("The data directory is the directory where all the data files will be stored ")
        print("if not provided the system will create the data directory in the current directory\n\n")


        print("please provide data directory (y,n):")
        ans = input()

        data_dir = ''

        if ans.lower() == 'y' or ans.lower() == 'yes':
            data_dir = input()

        if data_dir == '':
          data_dir = os.getcwd()

        #root directory
        pathlib.Path(data_dir + '/utranslate_data').mkdir(parents=True, exist_ok=True)

        #default data directory
        pathlib.Path(data_dir + '/utranslate_data/default_data').mkdir(parents=True, exist_ok=True)
        self.directory_handler.create_directories(self.data_types,data_dir + '/utranslate_data/default_data',True)

        #custom data directory
        pathlib.Path(data_dir + '/utranslate_data/custom_data').mkdir(parents=True, exist_ok=True)
        self.directory_handler.create_directories(self.data_types,data_dir + '/utranslate_data/custom_data')

        #translation data directory
        translations = ['hi_to_en','en_to_hi']
        self.directory_handler.create_translation_data_directory(data_dir,translations)

        #data directory
        self.root_dir = data_dir + '/utranslate_data'



    def download_files(self):

        self.data_dir = os.environ.get('utranslate_data_path') + '/default_data'

        #downloading the hindi word embeddings...
        urllib.request.urlretrieve('https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.hi.300.vec.gz',self.data_dir+'/cc.hi.300.vec.gz')

        #downloading the english word embeddings...
        urllib.request.urlretrieve('https://dl.fbaipublicfiles.com/fasttext/vectors-english/crawl-300d-2M.vec.zip',self.data_dir+'/crawl-300d-2M.vec.zip')

        #downloading the tranning data files...
        urllib.request.urlretrieve('https://www.cfilt.iitb.ac.in/~parallelcorp/iitb_en_hi_parallel/iitb_corpus_download/parallel.zip',self.data_dir+'/parallel.zip')
        # download the files from google drive
        # train_data_id_mankarvaibhav819 = '1w1NXPPbxRz8ANB4pevkI2C2eo6ounb-6'
        # train_save_dir = self.data_dir+'/parallel.zip'
        # self.downloader.download_file_from_google_drive(train_data_id_mankarvaibhav819,train_save_dir)
        



        #downloading the test data file...
        urllib.request.urlretrieve('https://www.cfilt.iitb.ac.in/~parallelcorp/iitb_en_hi_parallel/iitb_corpus_download/dev_test.zip',self.data_dir+'/dev_test.zip')
        # download the files from google drive
        # test_data_id_mankarvaibhav819 = '1ZNteg0PeVQC2ZqxnBMgdwWBca1cbn4mj'
        # test_save_dir = self.data_dir+'/dev_test.zip'
        # self.downloader.download_file_from_google_drive(test_data_id_mankarvaibhav819,test_save_dir)




        self.downloader.download_vocab_freq(self.data_dir)



    def download_predict(self,translator:int):

        translations = {0 : 'hi_to_en',
                        1 : 'en_to_hi'}


        data_dir =  os.environ.get('utranslate_data_path') + '/translation_data/' + translations[translator]
        
        self.downloader.download_embeddings(data_dir,translator)

        self.downloader.download_tokenizer(data_dir,translator)

        self.downloader.download_example_input_batch(data_dir,translator)

        self.downloader.download_config_file(data_dir,translator)

        self.downloader.download_checkpoints(data_dir,translator)


    def extract_files(self):
        self.extractor.extract_embeddings(self.data_dir)
        self.extractor.extract_data_files(self.data_dir)



    def read_write(self,src,dec):
        data_input = open(src[0],'r').readlines()
        data_target = open(src[1],'r').readlines()

        file_w_input = open(dec[0],'w')
        file_w_target = open(dec[1],'w')

        for input_line,target_line in zip(data_input,data_target):
            file_w_input.write(input_line)
            file_w_target.write(target_line)

        file_w_input.close()
        file_w_target.close()


    def populate_data_files(self):

        train = self.data_dir+'/Dataset/parallel-n/'
        test = self.data_dir+'/Dataset/dev_test/'

        Train_dir =self.data_dir+'/Dataset/train/'
        Eval_dir = self.data_dir+'/Dataset/eval/'
        Test_dir = self.data_dir+'/Dataset/test/'


        train_data_hi = open(train + 'IITB.en-hi.hi','r').readlines()
        train_data_en = open(train + 'IITB.en-hi.en','r').readlines()

        last_val = 0

        for name in self.data_types:

            file_hi  = open(Train_dir + name+'/input.txt','w')
            file_en  = open(Train_dir + name+'/target.txt','w')
            #print(name)
            val = last_val+self.data_types[name]

            for hi_line,en_line in zip(train_data_hi[last_val:val],train_data_en[last_val:val]):
              file_hi.write(hi_line)
              file_en.write(en_line)

            last_val=val

            file_hi.close()
            file_en.close()


        #eval
        eval_src = [test + 'dev.hi',test + 'dev.en']
        eval_dec = [Eval_dir + 'input.txt',Eval_dir + 'target.txt']

        self.read_write(eval_src,eval_dec)


        #test
        test_src = [test + 'test.hi',test + 'test.en']
        test_dec = [Test_dir + 'input.txt',Test_dir  + 'target.txt']

        self.read_write(test_src,test_dec)





    def clean_up(self):

      #remove compressed files
      os.remove(self.data_dir+'/cc.hi.300.vec.gz')
      os.remove(self.data_dir+'/dev_test.zip')
      os.remove(self.data_dir+'/crawl-300d-2M.vec.zip')
      os.remove(self.data_dir+'/parallel.zip')

      #remove unwanted folders
      shutil.rmtree(self.data_dir+'/Dataset/dev_test')
      shutil.rmtree(self.data_dir+'/Dataset/parallel-n')

