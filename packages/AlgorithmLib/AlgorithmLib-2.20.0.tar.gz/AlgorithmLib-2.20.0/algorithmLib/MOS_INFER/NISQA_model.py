# -*- coding: utf-8 -*-
"""
@author: Gabriel Mittag, TU-Berlin
"""
import time
import os
from glob import glob
import datetime
from pathlib import Path
import itertools

import numpy as np
import pandas as pd; pd.options.mode.chained_assignment=None
from tqdm import tqdm
import yaml
import torch
import torch.nn as nn
from torch import optim
from torch.utils.data import DataLoader
import NISQA_lib as NL
import sys

sys.path.append('../')
class nisqaModel(object):
    '''
    nisqaModel: Main class that loads the model and the datasets. Contains
    the training loop, prediction, and evaluation function.                                               
    '''      
    def __init__(self, args):
        self.args = args
        
        if 'mode' not in self.args:
            self.args['mode'] = 'main'
            
        self.runinfos = {}       
        self._getDevice()
        self._loadModel()
        self._loadDatasets()
        self.args['now'] = datetime.datetime.today()
        
        if self.args['mode']=='main':
            print(yaml.dump(self.args, default_flow_style=None, sort_keys=False))
            
        if self.args['task_type'] == 2:
            cp_path = './ssl/xlsr_53_56k.pt'
            model, cfg, task = fairseq.checkpoint_utils.load_model_ensemble_and_task([cp_path], arg_overrides={"best_checkpoint_metric": "wer"})
            model = model[0]
            model.eval()
            device = torch.device("cpu")
            model = model.to(device)
            self.model_ssl = model

    def train(self):
        
        if self.args['dim']==True:
            self._train_dim()
        elif self.args['task_type'] == 0:
            self._train_mos()    
        elif self.args['task_type'] == 1:
            self._train_multi_task()  
        elif self.args['task_type'] == 2:
            self._train_multi_feature() 
        elif self.args['task_type'] == 3:
            self._train_multi_resolution() 
        elif self.args['task_type'] == 4:
            self._train_multi_scale()  
            
    def evaluate(self, mapping='first_order', do_print=True, do_plot=False):
        if self.args['dim']==True:
            self._evaluate_dim(mapping=mapping, do_print=do_print, do_plot=do_plot)
        else:
            self._evaluate_mos(mapping=mapping, do_print=do_print, do_plot=do_plot)      
            
    def predict(self):
        print('---> Predicting ...')
        if self.args['tr_parallel']:
            self.model = nn.DataParallel(self.model)           
        
        if self.args['dim']==True:
            y_val_hat, y_val = NL.predict_dim(
                self.model, 
                self.ds_val, 
                self.args['tr_bs_val'],
                self.dev,
                num_workers=self.args['tr_num_workers'])
        else:
            if self.args['task_type'] == 0:
                y_val_hat, y_val = NL.predict_mos(
                    self.model, 
                    self.ds_val, 
                    self.args['tr_bs_val'],
                    self.dev,
                    num_workers=self.args['tr_num_workers']) 
            elif self.args['task_type'] == 1:
                y_val_hat, y_val = NL.predict_mos_multitask(
                    self.model, 
                    self.ds_val, 
                    self.args['tr_bs_val'],
                    self.dev,
                    num_workers=self.args['tr_num_workers']) 
            elif self.args['task_type'] == 2:
                y_val_hat, y_val = NL.predict_mos_multifeature(
                    self.model, 
                    self.ds_val, 
                    self.args['tr_bs_val'],
                    self.dev,
                    num_workers=self.args['tr_num_workers']) 
            elif self.args['task_type'] == 3:
                y_val_hat, y_val = NL.predict_mos_multiresolution(
                    self.model_1, 
                    self.model_2, 
                    self.model_3, 
                    self.ds_val, 
                    self.args['tr_bs_val'],
                    self.dev,
                    num_workers=self.args['tr_num_workers']) 
            elif self.args['task_type'] == 4:
                y_val_hat, y_val = NL.predict_mos_multiscale(
                    self.model_1, 
                    self.model_2, 
                    self.model_3, 
                    self.ds_val, 
                    self.args['tr_bs_val'],
                    self.dev,
                    num_workers=self.args['tr_num_workers']) 
            
        # import pdb; pdb.set_trace()        
        if self.args['output_dir']:
            self.ds_val.df['model'] = self.args['name']
            self.ds_val.df.to_csv(
                os.path.join(self.args['output_dir'], 'test.csv'),
                index=False)

            
        # print(self.ds_val.df.to_string(index=False))

        if self.args['task_type'] == 1:
            r_mos = NL.calc_eval_metrics(y_val[:,0].squeeze(), y_val_hat[:,0].squeeze())
            r_std = NL.calc_eval_metrics(y_val[:,1].squeeze(), y_val_hat[:,1].squeeze())
            print('mos')
            print(r_mos)
            print('std')
            print(r_std)
        else:
            r = NL.calc_eval_metrics(y_val.squeeze(), y_val_hat.squeeze())
            print(r)

        return self.ds_val.df

    def _train_mos(self):
        '''
        Trains speech quality model.
        '''
        # Initialize  -------------------------------------------------------------
        if self.args['tr_parallel']:
            self.model = nn.DataParallel(self.model)
        self.model.to(self.dev)

        # Runname and savepath  ---------------------------------------------------
        self.runname = self._makeRunnameAndWriteYAML()

        # Optimizer  -------------------------------------------------------------
        opt = optim.Adam(self.model.parameters(), lr=self.args['tr_lr'])        
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
                opt,
                'min',
                verbose=True,
                threshold=0.003,
                patience=self.args['tr_lr_patience'])
        earlyStp = NL.earlyStopper(self.args['tr_early_stop'])      
        
        biasLoss = NL.biasLoss(
            self.ds_train.df.database,
            anchor_db=self.args['tr_bias_anchor_db'], 
            mapping=self.args['tr_bias_mapping'], 
            min_r=self.args['tr_bias_min_r'],
            do_print=(self.args['tr_verbose']>0),
            )

        # Dataloader    -----------------------------------------------------------
        dl_train = DataLoader(
            self.ds_train,
            batch_size=self.args['tr_bs'],
            shuffle=True,
            drop_last=False,
            pin_memory=True,
            num_workers=self.args['tr_num_workers'])
        
        # Start training loop   ---------------------------------------------------
        print('--> start training')
        for epoch in range(self.args['tr_epochs']):

            tic_epoch = time.time()
            batch_cnt = 0
            loss = 0.0
            y_train = self.ds_train.df[self.args['csv_mos']].to_numpy().reshape(-1)
            y_train_hat = np.zeros((len(self.ds_train), 1))
            self.model.train()
            
            # Progress bar
            if self.args['tr_verbose'] == 2:
                pbar = tqdm(iterable=batch_cnt, total=len(dl_train), ascii=">—",
                            bar_format='{bar} {percentage:3.0f}%, {n_fmt}/{total_fmt}, {elapsed}<{remaining}{postfix}')
                
            for xb_spec, yb_mos, (idx, n_wins), yb_mos_std, yb_votes in dl_train:

                # Estimate batch ---------------------------------------------------
                xb_spec = xb_spec.to(self.dev)
                yb_mos = yb_mos.to(self.dev)
                n_wins = n_wins.to(self.dev)

                # Forward pass ----------------------------------------------------
                yb_mos_hat = self.model(xb_spec, n_wins)
                y_train_hat[idx] = yb_mos_hat.detach().cpu().numpy()

                # Loss ------------------------------------------------------------       
                lossb = biasLoss.get_loss(yb_mos, yb_mos_hat, idx)
                    
                # Backprop  -------------------------------------------------------
                lossb.backward()
                opt.step()
                opt.zero_grad()

                # Update total loss -----------------------------------------------
                loss += lossb.item()
                batch_cnt += 1

                if self.args['tr_verbose'] == 2:
                    pbar.set_postfix(loss=lossb.item())
                    pbar.update()

            if self.args['tr_verbose'] == 2:
                pbar.close()

            loss = loss/batch_cnt
            
            biasLoss.update_bias(y_train, y_train_hat)

            # Evaluate   -----------------------------------------------------------
            if self.args['tr_verbose']>0:
                print('\n<---- Training ---->')
            self.ds_train.df['mos_pred'] = y_train_hat
            db_results_train, r_train = NL.eval_results(
                self.ds_train.df, 
                dcon=self.ds_train.df_con, 
                target_mos=self.args['csv_mos'],
                target_ci=self.args['csv_mos'] + '_ci',
                pred='mos_pred',
                mapping = 'first_order',
                do_print=(self.args['tr_verbose']>0)
                )
            
            if self.args['tr_verbose']>0:
                print('<---- Validation ---->')
            NL.predict_mos(self.model, self.ds_val, self.args['tr_bs_val'], self.dev, num_workers=self.args['tr_num_workers'])
            db_results, r_val = NL.eval_results(
                self.ds_val.df, 
                dcon=self.ds_val.df_con, 
                target_mos=self.args['csv_mos'],
                target_ci=self.args['csv_mos'] + '_ci',
                pred='mos_pred',
                mapping = 'first_order',
                do_print=(self.args['tr_verbose']>0)
                )            
            
            r = {'train_pcc_mean_file': r_train['pcc_mean_file'],
                 'train_srcc_mean_file': r_train['srcc_mean_file'],
                 'train_rmse_map_mean_file': r_train['rmse_map_mean_file'],
                 **r_val}
            
            # Scheduler update    ---------------------------------------------
            scheduler.step(loss)
            earl_stp = earlyStp.step(r)            

            # Print    --------------------------------------------------------
            ep_runtime = time.time() - tic_epoch
            print(
                'ep {} sec {:0.0f} es {} lr {:0.0e} loss {:0.4f} // '
                'pcc_tr {:0.2f} srcc_tr {:0.2f} rmse_map_tr {:0.2f} // pcc_dev {:0.2f} srcc_dev {:0.2f} rmse_map_dev {:0.2f} // '
                'best_r_p {:0.2f} best_rmse {:0.2f},'
                .format(epoch+1, ep_runtime, earlyStp.cnt, NL.get_lr(opt), loss, 
                        r['train_pcc_mean_file'], r['train_srcc_mean_file'], r['train_rmse_map_mean_file'],
                        r['pcc_mean_file'],r['srcc_mean_file'], r['rmse_map_mean_file'],
                        earlyStp.best_r_p, earlyStp.best_rmse))

            # Save results and model  -----------------------------------------
            self._saveResults(self.model, self.model_args, opt, epoch, loss, ep_runtime, r, db_results, earlyStp.best)

            # Early stopping    -----------------------------------------------
            if earl_stp:
                print('--> Early stopping. best_r_p {:0.2f} best_rmse {:0.2f}'
                    .format(earlyStp.best_r_p, earlyStp.best_rmse))
                return        

        # Training done --------------------------------------------------------
        print('--> Training done. best_r_p {:0.2f} best_rmse_map {:0.2f}'
                            .format(earlyStp.best_r_p, earlyStp.best_rmse))        
        return        
     
    def _train_multi_task(self):
        '''
        Trains speech quality model.
        '''
        # Initialize  -------------------------------------------------------------
        if self.args['tr_parallel']:
            self.model = nn.DataParallel(self.model)
        self.model.to(self.dev)

        # Runname and savepath  ---------------------------------------------------
        self.runname = self._makeRunnameAndWriteYAML()

        # Optimizer  -------------------------------------------------------------
        opt = optim.Adam(self.model.parameters(), lr=self.args['tr_lr'])        
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
                opt,
                'min',
                verbose=True,
                threshold=0.003,
                patience=self.args['tr_lr_patience'])
        earlyStp = NL.earlyStopper_multitask(self.args['tr_early_stop'])      
        
        biasLoss_1 = NL.biasLoss(
            self.ds_train.df.database,
            anchor_db=self.args['tr_bias_anchor_db'], 
            mapping=self.args['tr_bias_mapping'], 
            min_r=self.args['tr_bias_min_r'],
            do_print=(self.args['tr_verbose']>0),
            )
        
        biasLoss_2 = NL.biasLoss(
            self.ds_train.df.database,
            anchor_db=self.args['tr_bias_anchor_db'], 
            mapping=self.args['tr_bias_mapping'], 
            min_r=self.args['tr_bias_min_r'],
            do_print=(self.args['tr_verbose']>0),
            )

        # Dataloader    -----------------------------------------------------------
        dl_train = DataLoader(
            self.ds_train,
            batch_size=self.args['tr_bs'],
            shuffle=True,
            drop_last=False,
            pin_memory=True,
            num_workers=self.args['tr_num_workers'])
        
        # Start training loop   ---------------------------------------------------
        print('--> start training')
        for epoch in range(self.args['tr_epochs']):

            tic_epoch = time.time()
            batch_cnt = 0
            loss = 0.0
            y_mos = self.ds_train.df['mos'].to_numpy().reshape(-1,1)
            y_std = self.ds_train.df['mos_std'].to_numpy().reshape(-1,1)
            y_train = np.concatenate((y_mos, y_std), axis=1)
        
            y_train_hat = np.zeros((len(self.ds_train), 2))
            self.model.train()
            
            # Progress bar
            if self.args['tr_verbose'] == 2:
                pbar = tqdm(iterable=batch_cnt, total=len(dl_train), ascii=">—",
                            bar_format='{bar} {percentage:3.0f}%, {n_fmt}/{total_fmt}, {elapsed}<{remaining}{postfix}')
                
            for xb_spec, yb_mos, (idx, n_wins), yb_mos_std, yb_votes in dl_train:

                # Estimate batch ---------------------------------------------------
                xb_spec = xb_spec.to(self.dev)
                yb_mos = yb_mos.to(self.dev)
                yb_mos_std = yb_mos_std.to(self.dev)
                n_wins = n_wins.to(self.dev)

                # Forward pass ----------------------------------------------------
                yb_mos_hat = self.model(xb_spec, n_wins)
                y_train_hat[idx,:] = yb_mos_hat.detach().cpu().numpy()

                # Loss ------------------------------------------------------------                       
                lossb_1 = biasLoss_1.get_loss(yb_mos, yb_mos_hat[:,0].view(-1,1), idx)
                lossb_2 = biasLoss_2.get_loss(yb_mos_std, yb_mos_hat[:,1].view(-1,1), idx)
          
                lossb = lossb_1 + 2 * lossb_2
       
                # Backprop  -------------------------------------------------------
                lossb.backward()
                opt.step()
                opt.zero_grad()

                # Update total loss -----------------------------------------------
                loss += lossb.item()
                batch_cnt += 1

                if self.args['tr_verbose'] == 2:
                    pbar.set_postfix(loss=lossb.item())
                    pbar.update()

            if self.args['tr_verbose'] == 2:
                pbar.close()

            loss = loss/batch_cnt
            
            biasLoss_1.update_bias(y_train[:,0].reshape(-1,1), y_train_hat[:,0].reshape(-1,1))
            biasLoss_2.update_bias(y_train[:,1].reshape(-1,1), y_train_hat[:,1].reshape(-1,1))

            # Evaluate   -----------------------------------------------------------
            self.ds_train.df['mos_pred'] = y_train_hat[:,0].reshape(-1,1)
            self.ds_train.df['std_pred'] = y_train_hat[:,1].reshape(-1,1)
            if self.args['tr_verbose']>0:
                print('\n<---- Training ---->')
            if self.args['tr_verbose']>0:
                print('--> MOS:')
            db_results_train_mos, r_train_mos = NL.eval_results(
                self.ds_train.df, 
                dcon=self.ds_train.df_con, 
                target_mos=self.args['csv_mos'],
                target_ci=self.args['csv_mos'] + '_ci',
                pred='mos_pred',
                mapping = 'first_order',
                do_print=(self.args['tr_verbose']>0)
                )
            
            if self.args['tr_verbose']>0:
                print('--> STD:')
            db_results_train_std, r_train_std = NL.eval_results(
                self.ds_train.df, 
                dcon=self.ds_train.df_con, 
                target_mos='mos_std',
                target_ci='mos_std_ci',
                pred='std_pred',
                mapping = 'first_order',
                do_print=(self.args['tr_verbose']>0)
                )      
            
            if self.args['tr_verbose']>0:
                print('<---- Validation ---->')
            NL.predict_mos_multitask(self.model, self.ds_val, self.args['tr_bs_val'], self.dev, num_workers=self.args['tr_num_workers'])
            
            if self.args['tr_verbose']>0:
                print('--> MOS:')
            db_results_val_mos, r_val_mos = NL.eval_results(
                self.ds_val.df, 
                dcon=self.ds_val.df_con, 
                target_mos='mos',
                target_ci='mos_ci',
                pred='mos_pred',
                mapping = 'first_order',
                do_print=(self.args['tr_verbose']>0)
                )    
            
            if self.args['tr_verbose']>0:
                print('--> STD:')
            db_results_val_std, r_val_std = NL.eval_results(
                self.ds_val.df, 
                dcon=self.ds_val.df_con, 
                target_mos='mos_std',
                target_ci='mos_std_ci',
                pred='std_pred',
                mapping = 'first_order',
                do_print=(self.args['tr_verbose']>0)
                )  
            r_val_std = {k+'_std': v for k, v in r_val_std.items()}         
            
            r = {'train_pcc_mean_file': r_train_mos['pcc_mean_file'],
                 'train_srcc_mean_file': r_train_mos['srcc_mean_file'],
                 'train_rmse_map_mean_file': r_train_mos['rmse_map_mean_file'],
                 
                 'train_pcc_mean_file_std': r_train_std['pcc_mean_file'],
                 'train_srcc_mean_file_std': r_train_std['srcc_mean_file'],
                 'train_rmse_map_mean_file_std': r_train_std['rmse_map_mean_file'],
                 **r_val_mos, **r_val_std}
            
            db_results = {
                'db_results_val_mos': db_results_val_mos,
                'db_results_val_std': db_results_val_std,}
            
            # Scheduler update    ---------------------------------------------
            scheduler.step(loss)
            earl_stp = earlyStp.step(r)            

            # Print    --------------------------------------------------------
            ep_runtime = time.time() - tic_epoch
        
            print(
                'ep {} sec {:0.0f} es {} lr {:0.0e} loss {:0.4f} // '
                'pcc_tr {:0.2f} srcc_tr {:0.2f} rmse_map_tr {:0.2f} // '
                'pcc_dev {:0.2f} srcc_dev {:0.2f} rmse_map_dev {:0.2f} // '
                'best_r_p {:0.2f} best_rmse {:0.2f},'
                .format(epoch+1, ep_runtime, earlyStp.cnt, NL.get_lr(opt), loss, 
                        r['train_pcc_mean_file'], r['train_srcc_mean_file'], r['train_rmse_map_mean_file'],
                        r['pcc_mean_file'],r['srcc_mean_file'], r['rmse_map_mean_file'],
                        earlyStp.best_r_p, earlyStp.best_rmse))

            # Save results and model  -----------------------------------------
            self._saveResults(self.model, self.model_args, opt, epoch, loss, ep_runtime, r, db_results, earlyStp.best)

            # Early stopping    -----------------------------------------------
            if earl_stp:
                print('--> Early stopping. best_r_p {:0.2f} best_rmse {:0.2f}'
                    .format(earlyStp.best_r_p, earlyStp.best_rmse))
                return        

        # Training done --------------------------------------------------------
        print('--> Training done. best_r_p {:0.2f} best_rmse_map {:0.2f}'
                            .format(earlyStp.best_r_p, earlyStp.best_rmse))        
        return  
    
    def _train_multi_feature(self):
        '''
        Trains speech quality model.
        '''
        # Initialize  -------------------------------------------------------------
        if self.args['tr_parallel']:
            self.model = nn.DataParallel(self.model)
        self.model.to(self.dev)

        # Runname and savepath  ---------------------------------------------------
        self.runname = self._makeRunnameAndWriteYAML()

        # Optimizer  -------------------------------------------------------------
        opt = optim.Adam(self.model.parameters(), lr=self.args['tr_lr'])        
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
                opt,
                'min',
                verbose=True,
                threshold=0.003,
                patience=self.args['tr_lr_patience'])
        earlyStp = NL.earlyStopper(self.args['tr_early_stop'])      
        
        biasLoss = NL.biasLoss(
            self.ds_train.df.database,
            anchor_db=self.args['tr_bias_anchor_db'], 
            mapping=self.args['tr_bias_mapping'], 
            min_r=self.args['tr_bias_min_r'],
            do_print=(self.args['tr_verbose']>0),
            )

        # Dataloader    -----------------------------------------------------------
        dl_train = DataLoader(
            self.ds_train,
            batch_size=self.args['tr_bs'],
            shuffle=True,
            drop_last=False,
            pin_memory=True,
            num_workers=self.args['tr_num_workers'])
        
        # Start training loop   ---------------------------------------------------
        print('--> start training')
        for epoch in range(self.args['tr_epochs']):

            tic_epoch = time.time()
            batch_cnt = 0
            loss = 0.0
            y_train = self.ds_train.df[self.args['csv_mos']].to_numpy().reshape(-1)
            y_train_hat = np.zeros((len(self.ds_train), 1))
            self.model.train()
            
            # Progress bar
            if self.args['tr_verbose'] == 2:
                pbar = tqdm(iterable=batch_cnt, total=len(dl_train), ascii=">—",
                            bar_format='{bar} {percentage:3.0f}%, {n_fmt}/{total_fmt}, {elapsed}<{remaining}{postfix}')
                
            for xb_spec, x_spec_ssl, yb_mos, (idx, n_wins), yb_mos_std, yb_votes in dl_train:

                # Estimate batch ---------------------------------------------------
                # import pdb; pdb.set_trace()
                feature = torch.cat((xb_spec, x_spec_ssl), -2)
                feature = feature.to(self.dev)
                # xb_spec = xb_spec.to(self.dev)
                # x_spec_ssl = x_spec_ssl.to(self.dev)
                yb_mos = yb_mos.to(self.dev)
                n_wins = n_wins.to(self.dev)
                
               

                # Forward pass ----------------------------------------------------
                yb_mos_hat = self.model(feature, n_wins)
                y_train_hat[idx] = yb_mos_hat.detach().cpu().numpy()

                # Loss ------------------------------------------------------------       
                lossb = biasLoss.get_loss(yb_mos, yb_mos_hat, idx)
                    
                # Backprop  -------------------------------------------------------
                lossb.backward()
                opt.step()
                opt.zero_grad()

                # Update total loss -----------------------------------------------
                loss += lossb.item()
                batch_cnt += 1

                if self.args['tr_verbose'] == 2:
                    pbar.set_postfix(loss=lossb.item())
                    pbar.update()

            if self.args['tr_verbose'] == 2:
                pbar.close()

            loss = loss/batch_cnt
            
            biasLoss.update_bias(y_train, y_train_hat)

            # Evaluate   -----------------------------------------------------------
            if self.args['tr_verbose']>0:
                print('\n<---- Training ---->')
            self.ds_train.df['mos_pred'] = y_train_hat
            db_results_train, r_train = NL.eval_results(
                self.ds_train.df, 
                dcon=self.ds_train.df_con, 
                target_mos=self.args['csv_mos'],
                target_ci=self.args['csv_mos'] + '_ci',
                pred='mos_pred',
                mapping = 'first_order',
                do_print=(self.args['tr_verbose']>0)
                )
            
            if self.args['tr_verbose']>0:
                print('<---- Validation ---->')
            NL.predict_mos_multifeature(self.model, self.ds_val, self.args['tr_bs_val'], self.dev, num_workers=self.args['tr_num_workers'])
            db_results, r_val = NL.eval_results(
                self.ds_val.df, 
                dcon=self.ds_val.df_con, 
                target_mos=self.args['csv_mos'],
                target_ci=self.args['csv_mos'] + '_ci',
                pred='mos_pred',
                mapping = 'first_order',
                do_print=(self.args['tr_verbose']>0)
                )            
            
            r = {'train_pcc_mean_file': r_train['pcc_mean_file'],
                 'train_srcc_mean_file': r_train['srcc_mean_file'],
                 'train_rmse_map_mean_file': r_train['rmse_map_mean_file'],
                 **r_val}
            
            # Scheduler update    ---------------------------------------------
            scheduler.step(loss)
            earl_stp = earlyStp.step(r)            

            # Print    --------------------------------------------------------
            ep_runtime = time.time() - tic_epoch
            print(
                'ep {} sec {:0.0f} es {} lr {:0.0e} loss {:0.4f} // '
                'pcc_tr {:0.2f} srcc_tr {:0.2f} rmse_map_tr {:0.2f} // pcc_dev {:0.2f} srcc_dev {:0.2f} rmse_map_dev {:0.2f} // '
                'best_r_p {:0.2f} best_rmse {:0.2f},'
                .format(epoch+1, ep_runtime, earlyStp.cnt, NL.get_lr(opt), loss, 
                        r['train_pcc_mean_file'], r['train_srcc_mean_file'], r['train_rmse_map_mean_file'],
                        r['pcc_mean_file'],r['srcc_mean_file'], r['rmse_map_mean_file'],
                        earlyStp.best_r_p, earlyStp.best_rmse))

            # Save results and model  -----------------------------------------
            self._saveResults(self.model, self.model_args, opt, epoch, loss, ep_runtime, r, db_results, earlyStp.best)

            # Early stopping    -----------------------------------------------
            if earl_stp:
                print('--> Early stopping. best_r_p {:0.2f} best_rmse {:0.2f}'
                    .format(earlyStp.best_r_p, earlyStp.best_rmse))
                return        

        # Training done --------------------------------------------------------
        print('--> Training done. best_r_p {:0.2f} best_rmse_map {:0.2f}'
                            .format(earlyStp.best_r_p, earlyStp.best_rmse))        
        return      
    
    def _train_multi_resolution(self):
        '''
        Trains speech quality model.
        '''
        # Initialize  -------------------------------------------------------------
        if self.args['tr_parallel']:
            self.model = nn.DataParallel(self.model)
        self.model_1.to(self.dev)
        self.model_2.to(self.dev)
        self.model_3.to(self.dev)

        # Runname and savepath  ---------------------------------------------------
        self.runname = self._makeRunnameAndWriteYAML()

        # Optimizer  -------------------------------------------------------------
        opt = optim.Adam(itertools.chain(self.model_1.parameters(), self.model_2.parameters(), self.model_3.parameters()), lr=self.args['tr_lr'])        
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
                opt,
                'min',
                verbose=True,
                threshold=0.003,
                patience=self.args['tr_lr_patience'])
        earlyStp = NL.earlyStopper(self.args['tr_early_stop'])      
        
        biasLoss = NL.biasLoss(
            self.ds_train.df.database,
            anchor_db=self.args['tr_bias_anchor_db'], 
            mapping=self.args['tr_bias_mapping'], 
            min_r=self.args['tr_bias_min_r'],
            do_print=(self.args['tr_verbose']>0),
            )

        # Dataloader    -----------------------------------------------------------
        dl_train = DataLoader(
            self.ds_train,
            batch_size=self.args['tr_bs'],
            shuffle=True,
            drop_last=False,
            pin_memory=True,
            num_workers=self.args['tr_num_workers'])
        
        # Start training loop   ---------------------------------------------------
        print('--> start training')
        for epoch in range(self.args['tr_epochs']):

            tic_epoch = time.time()
            batch_cnt = 0
            loss = 0.0
            y_train = self.ds_train.df[self.args['csv_mos']].to_numpy().reshape(-1)
            y_train_hat = np.zeros((len(self.ds_train), 1))
            self.model_1.train()
            self.model_2.train()
            self.model_3.train()
            
            # Progress bar
            if self.args['tr_verbose'] == 2:
                pbar = tqdm(iterable=batch_cnt, total=len(dl_train), ascii=">—",
                            bar_format='{bar} {percentage:3.0f}%, {n_fmt}/{total_fmt}, {elapsed}<{remaining}{postfix}')
                
            for xb_spec_1, xb_spec_2, xb_spec_3, yb_mos, (idx, n_wins_1, n_wins_2, n_wins_3), yb_mos_std, yb_votes in dl_train:

                # Estimate batch ---------------------------------------------------
                xb_spec_1 = xb_spec_1.to(self.dev)
                xb_spec_2 = xb_spec_2.to(self.dev)
                xb_spec_3 = xb_spec_3.to(self.dev)
                yb_mos = yb_mos.to(self.dev)
                n_wins_1 = n_wins_1.to(self.dev)
                n_wins_2 = n_wins_2.to(self.dev)
                n_wins_3 = n_wins_3.to(self.dev)
                                   
                # import pdb; pdb.set_trace()
                # Forward pass ----------------------------------------------------
                yb_mos_hat_1 = self.model_1(xb_spec_1, n_wins_1)
                yb_mos_hat_2 = self.model_2(xb_spec_2, n_wins_2)
                yb_mos_hat_3 = self.model_3(xb_spec_3, n_wins_3)
                yb_mos_hat = 1/3 * (yb_mos_hat_1 + yb_mos_hat_2 + yb_mos_hat_3)
                y_train_hat[idx] = yb_mos_hat.detach().cpu().numpy()

                # Loss ------------------------------------------------------------       
                lossb = biasLoss.get_loss(yb_mos, yb_mos_hat, idx)
                    
                # Backprop  -------------------------------------------------------
                lossb.backward()
                opt.step()
                opt.zero_grad()

                # Update total loss -----------------------------------------------
                loss += lossb.item()
                batch_cnt += 1

                if self.args['tr_verbose'] == 2:
                    pbar.set_postfix(loss=lossb.item())
                    pbar.update()

            if self.args['tr_verbose'] == 2:
                pbar.close()

            loss = loss/batch_cnt
            
            biasLoss.update_bias(y_train, y_train_hat)

            # Evaluate   -----------------------------------------------------------
            if self.args['tr_verbose']>0:
                print('\n<---- Training ---->')
            self.ds_train.df['mos_pred'] = y_train_hat
            db_results_train, r_train = NL.eval_results(
                self.ds_train.df, 
                dcon=self.ds_train.df_con, 
                target_mos=self.args['csv_mos'],
                target_ci=self.args['csv_mos'] + '_ci',
                pred='mos_pred',
                mapping = 'first_order',
                do_print=(self.args['tr_verbose']>0)
                )
            
            if self.args['tr_verbose']>0:
                print('<---- Validation ---->')
            NL.predict_mos_multiresolution(self.model_1, self.model_2, self.model_3, self.ds_val, self.args['tr_bs_val'], self.dev, num_workers=self.args['tr_num_workers'])
            db_results, r_val = NL.eval_results(
                self.ds_val.df, 
                dcon=self.ds_val.df_con, 
                target_mos=self.args['csv_mos'],
                target_ci=self.args['csv_mos'] + '_ci',
                pred='mos_pred',
                mapping = 'first_order',
                do_print=(self.args['tr_verbose']>0)
                )            
            
            r = {'train_pcc_mean_file': r_train['pcc_mean_file'],
                 'train_srcc_mean_file': r_train['srcc_mean_file'],
                 'train_rmse_map_mean_file': r_train['rmse_map_mean_file'],
                 **r_val}
            
            # Scheduler update    ---------------------------------------------
            scheduler.step(loss)
            earl_stp = earlyStp.step(r)            

            # Print    --------------------------------------------------------
            ep_runtime = time.time() - tic_epoch
            print(
                'ep {} sec {:0.0f} es {} lr {:0.0e} loss {:0.4f} // '
                'pcc_tr {:0.2f} srcc_tr {:0.2f} rmse_map_tr {:0.2f} // pcc_dev {:0.2f} srcc_dev {:0.2f} rmse_map_dev {:0.2f} // '
                'best_r_p {:0.2f} best_rmse {:0.2f},'
                .format(epoch+1, ep_runtime, earlyStp.cnt, NL.get_lr(opt), loss, 
                        r['train_pcc_mean_file'], r['train_srcc_mean_file'], r['train_rmse_map_mean_file'],
                        r['pcc_mean_file'],r['srcc_mean_file'], r['rmse_map_mean_file'],
                        earlyStp.best_r_p, earlyStp.best_rmse))

            # Save results and model  -----------------------------------------
            self._saveResults_multi(self.model_1, self.model_2, self.model_3, self.model_args, opt, epoch, loss, ep_runtime, r, db_results, earlyStp.best)

            # Early stopping    -----------------------------------------------
            if earl_stp:
                print('--> Early stopping. best_r_p {:0.2f} best_rmse {:0.2f}'
                    .format(earlyStp.best_r_p, earlyStp.best_rmse))
                return        

        # Training done --------------------------------------------------------
        print('--> Training done. best_r_p {:0.2f} best_rmse_map {:0.2f}'
                            .format(earlyStp.best_r_p, earlyStp.best_rmse))        
        return 
    
    def _train_multi_scale(self):
        '''
        Trains speech quality model.
        '''
        # Initialize  -------------------------------------------------------------
        if self.args['tr_parallel']:
            self.model = nn.DataParallel(self.model)
        self.model_1.to(self.dev)
        self.model_2.to(self.dev)
        self.model_3.to(self.dev)

        # Runname and savepath  ---------------------------------------------------
        self.runname = self._makeRunnameAndWriteYAML()

        # Optimizer  -------------------------------------------------------------
        opt = optim.Adam(itertools.chain(self.model_1.parameters(), self.model_2.parameters(), self.model_3.parameters()), lr=self.args['tr_lr'])        
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
                opt,
                'min',
                verbose=True,
                threshold=0.003,
                patience=self.args['tr_lr_patience'])
        earlyStp = NL.earlyStopper(self.args['tr_early_stop'])      
        
        biasLoss = NL.biasLoss(
            self.ds_train.df.database,
            anchor_db=self.args['tr_bias_anchor_db'], 
            mapping=self.args['tr_bias_mapping'], 
            min_r=self.args['tr_bias_min_r'],
            do_print=(self.args['tr_verbose']>0),
            )

        # Dataloader    -----------------------------------------------------------
        dl_train = DataLoader(
            self.ds_train,
            batch_size=self.args['tr_bs'],
            shuffle=True,
            drop_last=False,
            pin_memory=True,
            num_workers=self.args['tr_num_workers'])
        
        # Start training loop   ---------------------------------------------------
        print('--> start training')
        for epoch in range(self.args['tr_epochs']):

            tic_epoch = time.time()
            batch_cnt = 0
            loss = 0.0
            y_train = self.ds_train.df[self.args['csv_mos']].to_numpy().reshape(-1)
            y_train_hat = np.zeros((len(self.ds_train), 1))
            self.model_1.train()
            self.model_2.train()
            self.model_3.train()
            
            # Progress bar
            if self.args['tr_verbose'] == 2:
                pbar = tqdm(iterable=batch_cnt, total=len(dl_train), ascii=">—",
                            bar_format='{bar} {percentage:3.0f}%, {n_fmt}/{total_fmt}, {elapsed}<{remaining}{postfix}')
            
            # import pdb; pdb.set_trace()
            for sr, xb_spec_1, xb_spec_2, xb_spec_3, yb_mos, (idx, n_wins_1, n_wins_2, n_wins_3), yb_mos_std, yb_votes in dl_train:

                # Estimate batch ---------------------------------------------------
                sr = sr.to(self.dev)
                xb_spec_1 = xb_spec_1.to(self.dev)
                xb_spec_2 = xb_spec_2.to(self.dev)
                xb_spec_3 = xb_spec_3.to(self.dev)
                yb_mos = yb_mos.to(self.dev)
                n_wins_1 = n_wins_1.to(self.dev)
                n_wins_2 = n_wins_2.to(self.dev)
                n_wins_3 = n_wins_3.to(self.dev)

                
                xb_spec_1 = xb_spec_1[torch.nonzero(n_wins_1)].squeeze(1).float()
                xb_spec_2 = xb_spec_2[torch.nonzero(n_wins_2)].squeeze(1).float()
                xb_spec_3 = xb_spec_3[torch.nonzero(n_wins_3)].squeeze(1).float()
                
                n_wins_1_tmp = n_wins_1[torch.nonzero(n_wins_1)].squeeze(1).int()
                n_wins_2_tmp = n_wins_2[torch.nonzero(n_wins_2)].squeeze(1).int()
                n_wins_3_tmp = n_wins_3[torch.nonzero(n_wins_3)].squeeze(1).int()
                
                
                yb_mos_hat_1 = torch.zeros((sr.shape[0],1))
                yb_mos_hat_2 = torch.zeros((sr.shape[0],1))
                yb_mos_hat_3 = torch.zeros((sr.shape[0],1))
                yb_mos_hat = torch.zeros((sr.shape[0],1))
                
                yb_mos_hat_1 = yb_mos_hat_1.to(self.dev)
                yb_mos_hat_2 = yb_mos_hat_2.to(self.dev)
                yb_mos_hat_3 = yb_mos_hat_3.to(self.dev)
                yb_mos_hat = yb_mos_hat.to(self.dev)
                
                
                # Forward pass ----------------------------------------------------
                if n_wins_1_tmp.shape[0] > 1 :
                    tmp = self.model_1(xb_spec_1, n_wins_1_tmp)
                    yb_mos_hat_1[torch.nonzero(n_wins_1).squeeze(1)] = tmp  
                    
                if n_wins_2_tmp.shape[0] > 1 : 
                    tmp = self.model_2(xb_spec_2, n_wins_2_tmp)
                    yb_mos_hat_2[torch.nonzero(n_wins_2).squeeze(1)] = tmp  
                
                tmp = self.model_3(xb_spec_3, n_wins_3_tmp)
                yb_mos_hat_3[torch.nonzero(n_wins_3).squeeze(1)] = tmp  
     
                yb_mos_hat = yb_mos_hat_1 + yb_mos_hat_2 + yb_mos_hat_3
        
               
                count = torch.zeros(yb_mos_hat.shape)
                count = count.to(self.dev)
                for tmp in range(len(count)):
                    if sr[tmp] == 48000 or sr[tmp] == 44100:
                        count[tmp] = 3
                    elif sr[tmp] == 16000 or sr[tmp] == 32000:
                        count[tmp] = 2
                    else:
                        count[tmp] = 1
                      
                # import pdb; pdb.set_trace()
                yb_mos_hat = yb_mos_hat / count
                
                y_train_hat[idx] = yb_mos_hat.detach().cpu().numpy()

                # Loss ------------------------------------------------------------       
                lossb = biasLoss.get_loss(yb_mos, yb_mos_hat, idx)
                    
                # Backprop  -------------------------------------------------------
                lossb.backward()
                opt.step()
                opt.zero_grad()

                # Update total loss -----------------------------------------------
                loss += lossb.item()
                batch_cnt += 1

                if self.args['tr_verbose'] == 2:
                    pbar.set_postfix(loss=lossb.item())
                    pbar.update()

            if self.args['tr_verbose'] == 2:
                pbar.close()

            loss = loss/batch_cnt
            
            biasLoss.update_bias(y_train, y_train_hat)

            # Evaluate   -----------------------------------------------------------
            if self.args['tr_verbose']>0:
                print('\n<---- Training ---->')
            self.ds_train.df['mos_pred'] = y_train_hat
            db_results_train, r_train = NL.eval_results(
                self.ds_train.df, 
                dcon=self.ds_train.df_con, 
                target_mos=self.args['csv_mos'],
                target_ci=self.args['csv_mos'] + '_ci',
                pred='mos_pred',
                mapping = 'first_order',
                do_print=(self.args['tr_verbose']>0)
                )
            
            if self.args['tr_verbose']>0:
                print('<---- Validation ---->')
            NL.predict_mos_multiscale(self.model_1, self.model_2, self.model_3, self.ds_val, self.args['tr_bs_val'], self.dev, num_workers=self.args['tr_num_workers'])
            db_results, r_val = NL.eval_results(
                self.ds_val.df, 
                dcon=self.ds_val.df_con, 
                target_mos=self.args['csv_mos'],
                target_ci=self.args['csv_mos'] + '_ci',
                pred='mos_pred',
                mapping = 'first_order',
                do_print=(self.args['tr_verbose']>0)
                )            
            
            r = {'train_pcc_mean_file': r_train['pcc_mean_file'],
                 'train_srcc_mean_file': r_train['srcc_mean_file'],
                 'train_rmse_map_mean_file': r_train['rmse_map_mean_file'],
                 **r_val}
            
            # Scheduler update    ---------------------------------------------
            scheduler.step(loss)
            earl_stp = earlyStp.step(r)            

            # Print    --------------------------------------------------------
            ep_runtime = time.time() - tic_epoch
            print(
                'ep {} sec {:0.0f} es {} lr {:0.0e} loss {:0.4f} // '
                'pcc_tr {:0.2f} srcc_tr {:0.2f} rmse_map_tr {:0.2f} // pcc_dev {:0.2f} srcc_dev {:0.2f} rmse_map_dev {:0.2f} // '
                'best_r_p {:0.2f} best_rmse {:0.2f},'
                .format(epoch+1, ep_runtime, earlyStp.cnt, NL.get_lr(opt), loss, 
                        r['train_pcc_mean_file'], r['train_srcc_mean_file'], r['train_rmse_map_mean_file'],
                        r['pcc_mean_file'],r['srcc_mean_file'], r['rmse_map_mean_file'],
                        earlyStp.best_r_p, earlyStp.best_rmse))

            # Save results and model  -----------------------------------------
            self._saveResults_multi(self.model_1, self.model_2, self.model_3, self.model_args, opt, epoch, loss, ep_runtime, r, db_results, earlyStp.best)

            # Early stopping    -----------------------------------------------
            if earl_stp:
                print('--> Early stopping. best_r_p {:0.2f} best_rmse {:0.2f}'
                    .format(earlyStp.best_r_p, earlyStp.best_rmse))
                return        

        # Training done --------------------------------------------------------
        print('--> Training done. best_r_p {:0.2f} best_rmse_map {:0.2f}'
                            .format(earlyStp.best_r_p, earlyStp.best_rmse))        
        return
     
    def _train_dim(self):
        '''
        Trains multidimensional speech quality model.
        '''
        # Initialize  -------------------------------------------------------------
        if self.args['tr_parallel']:
            self.model = nn.DataParallel(self.model)
        self.model.to(self.dev)

        # Runname and savepath  ---------------------------------------------------
        self.runname = self._makeRunnameAndWriteYAML()

        # Optimizer  -------------------------------------------------------------
        opt = optim.Adam(self.model.parameters(), lr=self.args['tr_lr'])        
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
                opt,
                'min',
                verbose=True,
                threshold=0.003,
                patience=self.args['tr_lr_patience'])
        earlyStp = NL.earlyStopper_dim(self.args['tr_early_stop'])      
        
        biasLoss_1 = NL.biasLoss(
            self.ds_train.df.database,
            anchor_db=self.args['tr_bias_anchor_db'], 
            mapping=self.args['tr_bias_mapping'], 
            min_r=self.args['tr_bias_min_r'],
            do_print=(self.args['tr_verbose']>0),
            )
        
        biasLoss_2 = NL.biasLoss(
            self.ds_train.df.database,
            anchor_db=self.args['tr_bias_anchor_db'], 
            mapping=self.args['tr_bias_mapping'], 
            min_r=self.args['tr_bias_min_r'],
            do_print=(self.args['tr_verbose']>0),
            )
        
        biasLoss_3 = NL.biasLoss(
            self.ds_train.df.database,
            anchor_db=self.args['tr_bias_anchor_db'], 
            mapping=self.args['tr_bias_mapping'], 
            min_r=self.args['tr_bias_min_r'],
            do_print=(self.args['tr_verbose']>0),
            )
           
        biasLoss_4 = NL.biasLoss(
            self.ds_train.df.database,
            anchor_db=self.args['tr_bias_anchor_db'], 
            mapping=self.args['tr_bias_mapping'], 
            min_r=self.args['tr_bias_min_r'],
            do_print=(self.args['tr_verbose']>0),
            )
   
        biasLoss_5 = NL.biasLoss(
            self.ds_train.df.database,
            anchor_db=self.args['tr_bias_anchor_db'], 
            mapping=self.args['tr_bias_mapping'], 
            min_r=self.args['tr_bias_min_r'],
            do_print=(self.args['tr_verbose']>0),
            )
   
        # Dataloader    -----------------------------------------------------------
        dl_train = DataLoader(
            self.ds_train,
            batch_size=self.args['tr_bs'],
            shuffle=True,
            drop_last=False,
            pin_memory=True,
            num_workers=self.args['tr_num_workers'])
        
        
        # Start training loop   ---------------------------------------------------
        print('--> start training')
        for epoch in range(self.args['tr_epochs']):

            tic_epoch = time.time()
            batch_cnt = 0
            loss = 0.0
            y_mos = self.ds_train.df['mos'].to_numpy().reshape(-1,1)
            y_noi = self.ds_train.df['noi'].to_numpy().reshape(-1,1)
            y_dis = self.ds_train.df['dis'].to_numpy().reshape(-1,1)        
            y_col = self.ds_train.df['col'].to_numpy().reshape(-1,1)    
            y_loud = self.ds_train.df['loud'].to_numpy().reshape(-1,1)          
            y_train = np.concatenate((y_mos, y_noi, y_dis, y_col, y_loud), axis=1)
            y_train_hat = np.zeros((len(self.ds_train), 5))
                                    
            self.model.train()
            
            
            # Progress bar
            if self.args['tr_verbose'] == 2:
                pbar = tqdm(iterable=batch_cnt, total=len(dl_train), ascii=">—",
                            bar_format='{bar} {percentage:3.0f}%, {n_fmt}/{total_fmt}, {elapsed}<{remaining}{postfix}')
                
            for xb_spec, yb_mos, (idx, n_wins) in dl_train:

                # Estimate batch ---------------------------------------------------
                xb_spec = xb_spec.to(self.dev)
                yb_mos = yb_mos.to(self.dev)
                n_wins = n_wins.to(self.dev)
                
                # Forward pass ----------------------------------------------------
                yb_mos_hat = self.model(xb_spec, n_wins)
                y_train_hat[idx,:] = yb_mos_hat.detach().cpu().numpy()

                # Loss ------------------------------------------------------------                       
                lossb_1 = biasLoss_1.get_loss(yb_mos[:,0].view(-1,1), yb_mos_hat[:,0].view(-1,1), idx)
                lossb_2 = biasLoss_2.get_loss(yb_mos[:,1].view(-1,1), yb_mos_hat[:,1].view(-1,1), idx)
                lossb_3 = biasLoss_3.get_loss(yb_mos[:,2].view(-1,1), yb_mos_hat[:,2].view(-1,1), idx)
                lossb_4 = biasLoss_4.get_loss(yb_mos[:,3].view(-1,1), yb_mos_hat[:,3].view(-1,1), idx)
                lossb_5 = biasLoss_5.get_loss(yb_mos[:,4].view(-1,1), yb_mos_hat[:,4].view(-1,1), idx)
                
                lossb = lossb_1 + lossb_2 + lossb_3 + lossb_4 + lossb_5
                    
                # Backprop  -------------------------------------------------------
                lossb.backward()
                opt.step()
                opt.zero_grad()

                # Update total loss -----------------------------------------------
                loss += lossb.item()
                batch_cnt += 1

                if self.args['tr_verbose'] == 2:
                    pbar.set_postfix(loss=lossb.item())
                    pbar.update()

            if self.args['tr_verbose'] == 2:
                pbar.close()

            loss = loss/batch_cnt
     
            biasLoss_1.update_bias(y_train[:,0].reshape(-1,1), y_train_hat[:,0].reshape(-1,1))
            biasLoss_2.update_bias(y_train[:,1].reshape(-1,1), y_train_hat[:,1].reshape(-1,1))
            biasLoss_3.update_bias(y_train[:,2].reshape(-1,1), y_train_hat[:,2].reshape(-1,1))
            biasLoss_4.update_bias(y_train[:,3].reshape(-1,1), y_train_hat[:,3].reshape(-1,1))
            biasLoss_5.update_bias(y_train[:,4].reshape(-1,1), y_train_hat[:,4].reshape(-1,1))  
                
            # Evaluate   -----------------------------------------------------------
            self.ds_train.df['mos_pred'] = y_train_hat[:,0].reshape(-1,1)
            self.ds_train.df['noi_pred'] = y_train_hat[:,1].reshape(-1,1)
            self.ds_train.df['dis_pred'] = y_train_hat[:,2].reshape(-1,1)
            self.ds_train.df['col_pred'] = y_train_hat[:,3].reshape(-1,1)
            self.ds_train.df['loud_pred'] = y_train_hat[:,4].reshape(-1,1)
            
            if self.args['tr_verbose']>0:
                print('\n<---- Training ---->')
                print('--> MOS:')
            db_results_train_mos, r_train_mos = NL.eval_results(
                self.ds_train.df, 
                dcon=self.ds_train.df_con, 
                target_mos='mos',
                target_ci='mos_ci',
                pred='mos_pred',
                mapping = 'first_order',
                do_print=(self.args['tr_verbose']>0)
                )
            
            if self.args['tr_verbose']>0:
                print('--> NOI:')
            db_results_train_noi, r_train_noi = NL.eval_results(
                self.ds_train.df, 
                dcon=self.ds_train.df_con, 
                target_mos='noi',
                target_ci='noi_ci',
                pred='noi_pred',
                mapping = 'first_order',
                do_print=(self.args['tr_verbose']>0)
                )            
            
            if self.args['tr_verbose']>0:
                print('--> DIS:')
            db_results_train_dis, r_train_dis = NL.eval_results(
                self.ds_train.df, 
                dcon=self.ds_train.df_con, 
                target_mos='dis',
                target_ci='dis_ci',
                pred='dis_pred',
                mapping = 'first_order',
                do_print=(self.args['tr_verbose']>0)
                )            
            
            if self.args['tr_verbose']>0:
                print('--> COL:')
            db_results_train_col, r_train_col = NL.eval_results(
                self.ds_train.df, 
                dcon=self.ds_train.df_con, 
                target_mos='col',
                target_ci='col_ci',
                pred='col_pred',
                mapping = 'first_order',
                do_print=(self.args['tr_verbose']>0)
                )      
            
            if self.args['tr_verbose']>0:
                print('--> LOUD:')
            db_results_train_loud, r_train_loud = NL.eval_results(
                self.ds_train.df, 
                dcon=self.ds_train.df_con, 
                target_mos='loud',
                target_ci='loud_ci',
                pred='loud_pred',
                mapping = 'first_order',
                do_print=(self.args['tr_verbose']>0)
                )           
            
            NL.predict_dim(self.model, self.ds_val, self.args['tr_bs_val'], self.dev, num_workers=self.args['tr_num_workers'])
            
            if self.args['tr_verbose']>0:
                print('<---- Validation ---->')
                print('--> MOS:')
            db_results_val_mos, r_val_mos = NL.eval_results(
                self.ds_val.df, 
                dcon=self.ds_val.df_con, 
                target_mos='mos',
                target_ci='mos_ci',
                pred='mos_pred',
                mapping = 'first_order',
                do_print=(self.args['tr_verbose']>0)
                )    
            
            if self.args['tr_verbose']>0:
                print('--> NOI:')
            db_results_val_noi, r_val_noi = NL.eval_results(
                self.ds_val.df, 
                dcon=self.ds_val.df_con, 
                target_mos='noi',
                target_ci='noi_ci',
                pred='noi_pred',
                mapping = 'first_order',
                do_print=(self.args['tr_verbose']>0)
                )           
            r_val_noi = {k+'_noi': v for k, v in r_val_noi.items()}
            
            if self.args['tr_verbose']>0:
                print('--> DIS:')
            db_results_val_dis, r_val_dis = NL.eval_results(
                self.ds_val.df, 
                dcon=self.ds_val.df_con, 
                target_mos='dis',
                target_ci='dis_ci',
                pred='dis_pred',
                mapping = 'first_order',
                do_print=(self.args['tr_verbose']>0)
                )          
            r_val_dis = {k+'_dis': v for k, v in r_val_dis.items()}
            
            if self.args['tr_verbose']>0:
                print('--> COL:')
            db_results_val_col, r_val_col = NL.eval_results(
                self.ds_val.df, 
                dcon=self.ds_val.df_con, 
                target_mos='col',
                target_ci='col_ci',
                pred='col_pred',
                mapping = 'first_order',
                do_print=(self.args['tr_verbose']>0)
                )      
            r_val_col = {k+'_col': v for k, v in r_val_col.items()}
            
            if self.args['tr_verbose']>0:
                print('--> LOUD:')
            db_results_val_loud, r_val_loud = NL.eval_results(
                self.ds_val.df, 
                dcon=self.ds_val.df_con, 
                target_mos='loud',
                target_ci='loud_ci',
                pred='loud_pred',
                mapping = 'first_order',
                do_print=(self.args['tr_verbose']>0)
                )            
            r_val_loud = {k+'_loud': v for k, v in r_val_loud.items()}
            
            r = {
                'train_r_p_mean_file': r_train_mos['r_p_mean_file'],
                 'train_rmse_map_mean_file': r_train_mos['rmse_map_mean_file'],
                 
                'train_r_p_mean_file_noi': r_train_noi['r_p_mean_file'],
                 'train_rmse_map_mean_file_noi': r_train_noi['rmse_map_mean_file'],

                'train_r_p_mean_file_dis': r_train_dis['r_p_mean_file'],
                 'train_rmse_map_mean_file_dis': r_train_dis['rmse_map_mean_file'],

                'train_r_p_mean_file_col': r_train_col['r_p_mean_file'],
                 'train_rmse_map_mean_file_col': r_train_col['rmse_map_mean_file'],

                'train_r_p_mean_file_loud': r_train_loud['r_p_mean_file'],
                 'train_rmse_map_mean_file_loud': r_train_loud['rmse_map_mean_file'],
                 
                 **r_val_mos, **r_val_noi, **r_val_dis, **r_val_col, **r_val_loud, }
            
            db_results = {
                'db_results_val_mos': db_results_val_mos,
                'db_results_val_noi': db_results_val_noi,
                'db_results_val_dis': db_results_val_dis,
                'db_results_val_col': db_results_val_col,
                'db_results_val_loud': db_results_val_loud
                          }             
            
            # Scheduler update    ---------------------------------------------
            scheduler.step(loss)
            earl_stp = earlyStp.step(r)            

            # Print    --------------------------------------------------------
            ep_runtime = time.time() - tic_epoch

            r_dim_mos_mean = 1/5 * (r['r_p_mean_file'] + 
                      r['r_p_mean_file_noi'] +
                      r['r_p_mean_file_col'] +
                      r['r_p_mean_file_dis'] +
                      r['r_p_mean_file_loud'])

            print(
                'ep {} sec {:0.0f} es {} lr {:0.0e} loss {:0.4f} // '
                'r_p_tr {:0.2f} rmse_map_tr {:0.2f} // r_dim_mos_mean {:0.2f}, r_p {:0.2f} rmse_map {:0.2f} // '
                'best_r_p {:0.2f} best_rmse_map {:0.2f},'
                .format(epoch+1, ep_runtime, earlyStp.cnt, NL.get_lr(opt), loss, 
                        r['train_r_p_mean_file'], r['train_rmse_map_mean_file'],
                        r_dim_mos_mean,
                        r['r_p_mean_file'], r['rmse_map_mean_file'],
                        earlyStp.best_r_p, earlyStp.best_rmse))

            # Save results and model  -----------------------------------------
            self._saveResults(self.model, self.model_args, opt, epoch, loss, ep_runtime, r, db_results, earlyStp.best)

            # Early stopping    -----------------------------------------------
            if earl_stp:
                print('--> Early stopping. best_r_p {:0.2f} best_rmse {:0.2f}'
                    .format(earlyStp.best_r_p, earlyStp.best_rmse))
                return        

        # Training done --------------------------------------------------------
        print('--> Training done. best_r_p {:0.2f} best_rmse {:0.2f}'
                            .format(earlyStp.best_r_p, earlyStp.best_rmse))        
        return        
            
    
    def _evaluate_mos(self, mapping='first_order', do_print=True, do_plot=False):
        '''
        Evaluates the model's predictions.
        '''        
        print('--> MOS:')
        self.db_results, self.r = NL.eval_results(
            self.ds_val.df,
            dcon=self.ds_val.df_con,
            target_mos='mos',
            target_ci='mos_ci',
            pred='mos_pred',
            mapping=mapping,
            do_print=do_print,
            do_plot=do_plot
            )
        if self.ds_val.df_con is None:
            print('r_p_mean_file: {:0.2f}, rmse_mean_file: {:0.2f}'
                .format(self.r['r_p_mean_file'], self.r['rmse_mean_file'])
                )                  
        else:
            print('r_p_mean_con: {:0.2f}, rmse_mean_con: {:0.2f}, rmse_star_map_mean_con: {:0.2f}'
                .format(self.r['r_p_mean_con'], self.r['rmse_mean_con'], self.r['rmse_star_map_mean_con'])
                )             
    
    def _evaluate_dim(self, mapping='first_order', do_print=True, do_plot=False):
        '''
        Evaluates the predictions of a multidimensional model.
        '''            
        print('--> MOS:')
        self.db_results_val_mos, r_val_mos = NL.eval_results(
            self.ds_val.df, 
            dcon=self.ds_val.df_con, 
            target_mos='mos',
            target_ci='mos_ci',
            pred='mos_pred',
            mapping=mapping,
            do_print=do_print,
            do_plot=do_plot
            )       
        if self.ds_val.df_con is None:
            print('r_p_mean_file: {:0.2f}, rmse_mean_file: {:0.2f}'
                .format(r_val_mos['r_p_mean_file'], r_val_mos['rmse_mean_file'])
                )                  
        else:
            print('r_p_mean_con: {:0.2f}, rmse_mean_con: {:0.2f}, rmse_star_map_mean_con: {:0.2f}'
                .format(r_val_mos['r_p_mean_con'], r_val_mos['rmse_mean_con'], r_val_mos['rmse_star_map_mean_con'])
                )    
                
        print('--> NOI:')
        self.db_results_val_noi, r_val_noi = NL.eval_results(
            self.ds_val.df, 
            dcon=self.ds_val.df_con, 
            target_mos='noi',
            target_ci='noi_ci',
            pred='noi_pred',
            mapping=mapping,
            do_print=do_print,
            do_plot=do_plot
            )  
        if self.ds_val.df_con is None:
            print('r_p_mean_file: {:0.2f}, rmse_mean_file: {:0.2f}'
                .format(r_val_noi['r_p_mean_file'], r_val_noi['rmse_mean_file'])
                )                  
        else:
            print('r_p_mean_con: {:0.2f}, rmse_mean_con: {:0.2f}'
                .format(r_val_noi['r_p_mean_con'], r_val_noi['rmse_mean_con'], r_val_noi['rmse_star_map_mean_con'])
                )            
        r_val_noi = {k+'_noi': v for k, v in r_val_noi.items()}
        
        print('--> DIS:')
        self.db_results_val_dis, r_val_dis = NL.eval_results(
            self.ds_val.df, 
            dcon=self.ds_val.df_con, 
            target_mos='dis',
            target_ci='dis_ci',
            pred='dis_pred',
            mapping=mapping,
            do_print=do_print,
            do_plot=do_plot
            )
        if self.ds_val.df_con is None:
            print('r_p_mean_file: {:0.2f}, rmse_mean_file: {:0.2f}'
                .format(r_val_dis['r_p_mean_file'], r_val_dis['rmse_mean_file'])
                )                  
        else:
            print('r_p_mean_con: {:0.2f}, rmse_mean_con: {:0.2f}, rmse_star_map_mean_con: {:0.2f}'
                .format(r_val_dis['r_p_mean_con'], r_val_dis['rmse_mean_con'], r_val_dis['rmse_star_map_mean_con'])
                )               
        r_val_dis = {k+'_dis': v for k, v in r_val_dis.items()}
        
        print('--> COL:')
        self.db_results_val_col, r_val_col = NL.eval_results(
            self.ds_val.df, 
            dcon=self.ds_val.df_con, 
            target_mos='col',
            target_ci='col_ci',
            pred='col_pred',
            mapping=mapping,
            do_print=do_print,
            do_plot=do_plot
            )  
        if self.ds_val.df_con is None:
            print('r_p_mean_file: {:0.2f}, rmse_mean_file: {:0.2f}'
                .format(r_val_col['r_p_mean_file'], r_val_col['rmse_mean_file'])
                )                  
        else:
            print('r_p_mean_con: {:0.2f}, rmse_mean_con: {:0.2f}, rmse_star_map_mean_con: {:0.2f}'
                .format(r_val_col['r_p_mean_con'], r_val_col['rmse_mean_con'], r_val_col['rmse_star_map_mean_con'])
                )            
        r_val_col = {k+'_col': v for k, v in r_val_col.items()}
        
        print('--> LOUD:')
        self.db_results_val_loud, r_val_loud = NL.eval_results(
            self.ds_val.df, 
            dcon=self.ds_val.df_con, 
            target_mos='loud',
            target_ci='loud_ci',
            pred='loud_pred',
            mapping=mapping,
            do_print=do_print,
            do_plot=do_plot
            )
        if self.ds_val.df_con is None:
            print('r_p_mean_file: {:0.2f}, rmse_mean_file: {:0.2f}'
                .format(r_val_loud['r_p_mean_file'], r_val_loud['rmse_mean_file'])
                )                  
        else:
            print('r_p_mean_con: {:0.2f}, rmse_mean_con: {:0.2f}, rmse_star_map_mean_con: {:0.2f}'
                .format(r_val_loud['r_p_mean_con'], r_val_loud['rmse_mean_con'], r_val_loud['rmse_star_map_mean_con'])
                )                    
        r_val_loud = {k+'_loud': v for k, v in r_val_loud.items()}
        
        self.r = {             
             **r_val_mos, **r_val_noi, **r_val_dis, **r_val_col, **r_val_loud, }            
        
        r_mean = 1/5 * (self.r['r_p_mean_con'] + 
                  self.r['r_p_mean_con_noi'] +
                  self.r['r_p_mean_con_col'] +
                  self.r['r_p_mean_con_dis'] +
                  self.r['r_p_mean_con_loud'])
                  
        print('\nAverage over MOS and dimensions: r_p={:0.3f}'
            .format(r_mean)
            )
                

    def _makeRunnameAndWriteYAML(self):
        '''
        Creates individual run name.
        '''        
        runname = self.args['name'] + '_' + self.args['now'].strftime("%y%m%d_%H%M%S%f")
        print('runname: ' + runname)
        run_output_dir = os.path.join(self.args['output_dir'], runname)
        Path(run_output_dir).mkdir(parents=True, exist_ok=True)
        yaml_path = os.path.join(run_output_dir, runname+'.yaml')
        with open(yaml_path, 'w') as file:
            yaml.dump(self.args, file, default_flow_style=None, sort_keys=False)          

        return runname
    
    def _loadDatasets(self):
        if self.args['mode']=='predict_file':
            self._loadDatasetsFile()
        elif self.args['mode']=='predict_dir':
            self._loadDatasetsFolder()  
        elif self.args['mode']=='predict_csv':
            self._loadDatasetsCSVpredict()
        elif self.args['mode']=='main':
            self._loadDatasetsCSV()
        else:
            raise NotImplementedError('mode not available')                        
            
    
    def _loadDatasetsFolder(self):
        files = glob( os.path.join(self.args['data_dir'], '*.wav') )
        files = [os.path.basename(files) for files in files]
        df_val = pd.DataFrame(files, columns=['deg'])
     
        print('# files: {}'.format( len(df_val) ))
        if len(df_val)==0:
            raise ValueError('No wav files found in data_dir')   
        
        # creating Datasets ---------------------------------------------------                        
        self.ds_val = NL.SpeechQualityDataset(
            df_val,
            df_con=None,
            data_dir = self.args['data_dir'],
            filename_column = 'deg',
            mos_column = 'predict_only',              
            seg_length = self.args['ms_seg_length'],
            max_length = self.args['ms_max_segments'],
            to_memory = None,
            to_memory_workers = None,
            seg_hop_length = self.args['ms_seg_hop_length'],
            transform = None,
            ms_n_fft = self.args['ms_n_fft'],
            ms_hop_length = self.args['ms_hop_length'],
            ms_win_length = self.args['ms_win_length'],
            ms_n_mels = self.args['ms_n_mels'],
            ms_sr = self.args['ms_sr'],
            ms_fmax = self.args['ms_fmax'],
            ms_channel = self.args['ms_channel'],
            double_ended = self.args['double_ended'],
            dim = self.args['dim'],
            filename_column_ref = None,
            mos_std_column = 'mos_std',
            votes_column = 'votes',
            task_type = self.args['task_type'],
            )
        
        
    def _loadDatasetsFile(self):
        data_dir = os.path.dirname(self.args['deg'])
        file_name = os.path.basename(self.args['deg'])        
        df_val = pd.DataFrame([file_name], columns=['deg'])
                
        # creating Datasets ---------------------------------------------------                        
        self.ds_val = NL.SpeechQualityDataset(
            df_val,
            df_con=None,
            data_dir = data_dir,
            filename_column = 'deg',
            mos_column = 'predict_only',              
            seg_length = self.args['ms_seg_length'],
            max_length = self.args['ms_max_segments'],
            to_memory = None,
            to_memory_workers = None,
            seg_hop_length = self.args['ms_seg_hop_length'],
            transform = None,
            ms_n_fft = self.args['ms_n_fft'],
            ms_hop_length = self.args['ms_hop_length'],
            ms_win_length = self.args['ms_win_length'],
            ms_n_mels = self.args['ms_n_mels'],
            ms_sr = self.args['ms_sr'],
            ms_fmax = self.args['ms_fmax'],
            ms_channel = self.args['ms_channel'],
            double_ended = self.args['double_ended'],
            dim = self.args['dim'],
            filename_column_ref = None,
            mos_std_column = 'mos_std',
            votes_column = 'votes',
            task_type = self.args['task_type'],
        )
                
        
    def _loadDatasetsCSVpredict(self):         
        '''
        Loads validation dataset for prediction only.
        '''            
        csv_file_path = os.path.join(self.args['data_dir'], self.args['csv_file'])
        dfile = pd.read_csv(csv_file_path)
        dcon = None
        '''
        if 'csv_con' in self.args:
            csv_con_file_path = os.path.join(self.args['data_dir'], self.args['csv_con'])
            dcon = pd.read_csv(csv_con_file_path)        
        else:
            dcon = None
        '''
        

        # creating Datasets ---------------------------------------------------                        
        self.ds_val = NL.SpeechQualityDataset(
            dfile,
            df_con=dcon,
            data_dir = self.args['data_dir'],
            filename_column = self.args['csv_deg'],
            mos_column = 'predict_only',
            seg_length = self.args['ms_seg_length'],
            max_length = self.args['ms_max_segments'],
            to_memory = False,
            to_memory_workers = None,
            seg_hop_length = self.args['ms_seg_hop_length'],
            transform = None,
            ms_n_fft = self.args['ms_n_fft'],
            ms_hop_length = self.args['ms_hop_length'],
            ms_win_length = self.args['ms_win_length'],
            ms_n_mels = self.args['ms_n_mels'],
            ms_sr = self.args['ms_sr'],
            ms_fmax = self.args['ms_fmax'],
            ms_channel = self.args['ms_channel'],
            double_ended = self.args['double_ended'],
            dim = self.args['dim'],
            filename_column_ref = self.args['csv_ref'],
            mos_std_column = 'mos_std',
            votes_column = 'votes',
            task_type = self.args['task_type'],
        )

        
    def _loadDatasetsCSV(self):    
        '''
        Loads training and validation dataset for training.
        '''          
        csv_file_path = os.path.join(self.args['data_dir'], self.args['csv_file'])
        dfile = pd.read_csv(csv_file_path)

        if not set(self.args['csv_db_train'] + self.args['csv_db_val']).issubset(dfile.database.unique().tolist()):
            missing_datasets = set(self.args['csv_db_train'] + self.args['csv_db_val']).difference(dfile.database.unique().tolist())
            raise ValueError('Not all dbs found in csv:', missing_datasets)

        df_train = dfile[dfile.database.isin(self.args['csv_db_train'])].reset_index()
        df_val = dfile[dfile.database.isin(self.args['csv_db_val'])].reset_index()
        
        if self.args['csv_con'] is not None:
            csv_con_path = os.path.join(self.args['data_dir'], self.args['csv_con'])
            dcon = pd.read_csv(csv_con_path)
            dcon_train = dcon[dcon.database.isin(self.args['csv_db_train'])].reset_index()
            dcon_val = dcon[dcon.database.isin(self.args['csv_db_val'])].reset_index()
        else:
            dcon = None        
            dcon_train = None        
            dcon_val = None        
        
        print('Training size: {}, Validation size: {}'.format(len(df_train), len(df_val)))
        
        # creating Datasets ---------------------------------------------------                        
        self.ds_train = NL.SpeechQualityDataset(
            df_train,
            df_con=dcon_train,
            data_dir = self.args['data_dir'],
            filename_column = self.args['csv_deg'],
            mos_column = self.args['csv_mos'],
            seg_length = self.args['ms_seg_length'],
            max_length = self.args['ms_max_segments'],
            to_memory = self.args['tr_ds_to_memory'],
            to_memory_workers = self.args['tr_ds_to_memory_workers'],
            seg_hop_length = self.args['ms_seg_hop_length'],
            transform = None,
            ms_n_fft = self.args['ms_n_fft'],
            ms_hop_length = self.args['ms_hop_length'],
            ms_win_length = self.args['ms_win_length'],
            ms_n_mels = self.args['ms_n_mels'],
            ms_sr = self.args['ms_sr'],
            ms_fmax = self.args['ms_fmax'],
            ms_channel = self.args['ms_channel'],
            double_ended = self.args['double_ended'],
            dim = self.args['dim'],
            filename_column_ref = self.args['csv_ref'],
            mos_std_column = self.args['csv_mos_std'],
            votes_column = self.args['csv_votes'],
            task_type = self.args['task_type'],
        )

        self.ds_val = NL.SpeechQualityDataset(
            df_val,
            df_con=dcon_val,
            data_dir = self.args['data_dir'],
            filename_column = self.args['csv_deg'],
            mos_column = self.args['csv_mos'],
            seg_length = self.args['ms_seg_length'],
            max_length = self.args['ms_max_segments'],
            to_memory = self.args['tr_ds_to_memory'],
            to_memory_workers = self.args['tr_ds_to_memory_workers'],
            seg_hop_length = self.args['ms_seg_hop_length'],
            transform = None,
            ms_n_fft = self.args['ms_n_fft'],
            ms_hop_length = self.args['ms_hop_length'],
            ms_win_length = self.args['ms_win_length'],
            ms_n_mels = self.args['ms_n_mels'],
            ms_sr = self.args['ms_sr'],
            ms_fmax = self.args['ms_fmax'],
            ms_channel = self.args['ms_channel'],
            double_ended = self.args['double_ended'],
            dim = self.args['dim'],
            filename_column_ref = self.args['csv_ref'],
            mos_std_column=self.args['csv_mos_std'],
            votes_column=self.args['csv_votes'],
            task_type = self.args['task_type'],
            )

        self.runinfos['ds_train_len'] = len(self.ds_train)
        self.runinfos['ds_val_len'] = len(self.ds_val)
    
    def _loadModel(self):    
        '''
        Loads the Pytorch models with given input arguments.
        '''   
        # if True overwrite input arguments from pretrained model
        # import pdb; pdb.set_trace()
        if self.args['pretrained_model']:
            # if os.path.isabs(self.args['pretrained_model']):
            #     model_path = os.path.join(self.args['pretrained_model'])
            # else:
            #     model_path = os.path.join(os.getcwd(), self.args['pretrained_model'])
            model_path = os.path.join(sys.prefix, self.args['pretrained_model'])
            if self.args['task_type'] == 3 or self.args['task_type'] == 4:
                checkpoint = torch.load(model_path[:-4] + '_1.tar', map_location=self.dev)
                checkpoint_2 = torch.load(model_path[:-4] + '_2.tar', map_location=self.dev)
                checkpoint_3 = torch.load(model_path[:-4] + '_3.tar', map_location=self.dev)
                
            else:
                checkpoint = torch.load(model_path, map_location=self.dev)
            
            # update checkpoint arguments with new arguments
            checkpoint['args'].update(self.args)
            self.args = checkpoint['args']
            
        if self.args['model']=='NISQA_DIM':
            self.args['dim'] = True
            self.args['csv_mos'] = None # column names hardcoded for dim models
        else:
            self.args['dim'] = False
            
        if self.args['model']=='NISQA_DE':
            self.args['double_ended'] = True
        else:
            self.args['double_ended'] = False     
            self.args['csv_ref'] = None

        # Load Model
        self.model_args = {
            
            'ms_seg_length': self.args['ms_seg_length'],
            'ms_n_mels': self.args['ms_n_mels'],
            
            'cnn_model': self.args['cnn_model'],
            'cnn_c_out_1': self.args['cnn_c_out_1'],
            'cnn_c_out_2': self.args['cnn_c_out_2'],
            'cnn_c_out_3': self.args['cnn_c_out_3'],
            'cnn_kernel_size': self.args['cnn_kernel_size'],
            'cnn_dropout': self.args['cnn_dropout'],
            'cnn_pool_1': self.args['cnn_pool_1'],
            'cnn_pool_2': self.args['cnn_pool_2'],
            'cnn_pool_3': self.args['cnn_pool_3'],
            'cnn_fc_out_h': self.args['cnn_fc_out_h'],
            
            'td': self.args['td'],
            'td_sa_d_model': self.args['td_sa_d_model'],
            'td_sa_nhead': self.args['td_sa_nhead'],
            'td_sa_pos_enc': self.args['td_sa_pos_enc'],
            'td_sa_num_layers': self.args['td_sa_num_layers'],
            'td_sa_h': self.args['td_sa_h'],
            'td_sa_dropout': self.args['td_sa_dropout'],
            'td_lstm_h': self.args['td_lstm_h'],
            'td_lstm_num_layers': self.args['td_lstm_num_layers'],
            'td_lstm_dropout': self.args['td_lstm_dropout'],
            'td_lstm_bidirectional': self.args['td_lstm_bidirectional'],
            
            'td_2': self.args['td_2'],
            'td_2_sa_d_model': self.args['td_2_sa_d_model'],
            'td_2_sa_nhead': self.args['td_2_sa_nhead'],
            'td_2_sa_pos_enc': self.args['td_2_sa_pos_enc'],
            'td_2_sa_num_layers': self.args['td_2_sa_num_layers'],
            'td_2_sa_h': self.args['td_2_sa_h'],
            'td_2_sa_dropout': self.args['td_2_sa_dropout'],
            'td_2_lstm_h': self.args['td_2_lstm_h'],
            'td_2_lstm_num_layers': self.args['td_2_lstm_num_layers'],
            'td_2_lstm_dropout': self.args['td_2_lstm_dropout'],
            'td_2_lstm_bidirectional': self.args['td_2_lstm_bidirectional'],                
            
            'pool': self.args['pool'],
            'pool_att_h': self.args['pool_att_h'],
            'pool_att_dropout': self.args['pool_att_dropout'],
            }
            
        if self.args['double_ended']:
            self.model_args.update({
                'de_align': self.args['de_align'],
                'de_align_apply': self.args['de_align_apply'],
                'de_fuse_dim': self.args['de_fuse_dim'],
                'de_fuse': self.args['de_fuse'],        
                })
                      
        print('Model architecture: ' + self.args['model'])
        if self.args['model']=='NISQA':
            if self.args['task_type'] == 0:
                self.model = NL.NISQA(**self.model_args)     
            elif self.args['task_type'] == 1:
                self.model = NL.NISQA_MULTITASK(**self.model_args)
            elif self.args['task_type'] == 2:
                self.model = NL.NISQA(**self.model_args) 
            elif self.args['task_type'] == 3:
                self.model_1 = NL.NISQA(**self.model_args)  
                self.model_2 = NL.NISQA(**self.model_args) 
                self.model_3 = NL.NISQA(**self.model_args)
            elif self.args['task_type'] == 4:
                self.model_1 = NL.NISQA(**self.model_args)  
                self.model_2 = NL.NISQA(**self.model_args) 
                self.model_3 = NL.NISQA(**self.model_args) 
                
        elif self.args['model']=='NISQA_DIM':
            self.model = NL.NISQA_DIM(**self.model_args)     
        elif self.args['model']=='NISQA_DE':
            self.model = NL.NISQA_DE(**self.model_args)     
        else:
            raise NotImplementedError('Model not available')                        
        
        
        # Load weights if pretrained model is used ------------------------------------
        if self.args['pretrained_model']:
            if self.args['task_type'] == 3 or self.args['task_type'] == 4:
                missing_keys, unexpected_keys = self.model_1.load_state_dict(checkpoint['model_state_dict'], strict=True)
                missing_keys, unexpected_keys = self.model_2.load_state_dict(checkpoint_2['model_state_dict'], strict=True)
                missing_keys, unexpected_keys = self.model_3.load_state_dict(checkpoint_3['model_state_dict'], strict=True)
            else:
                missing_keys, unexpected_keys = self.model.load_state_dict(checkpoint['model_state_dict'], strict=True)
            print('Loaded pretrained model from ' + self.args['pretrained_model'])
            if missing_keys:
                print('missing_keys:')
                print(missing_keys)
            if unexpected_keys:
                print('unexpected_keys:')
                print(unexpected_keys)  
                
        # para_num = sum([p.numel() for p in self.model.parameters()])
        # para_size = para_num * 4 / 1024
        # import pdb; pdb.set_trace()
        
        
    def _getDevice(self):
        '''
        Train on GPU if available.
        '''         
        if torch.cuda.is_available():
            self.dev = torch.device("cuda")
        else:
            self.dev = torch.device("cpu")
    
        if "tr_device" in self.args:
            if self.args['tr_device']=='cpu':
                self.dev = torch.device("cpu")
            elif self.args['tr_device']=='cuda':
                self.dev = torch.device("cuda")
        print('Device: {}'.format(self.dev))
        
        if "tr_parallel" in self.args:
            if (self.dev==torch.device("cpu")) and self.args['tr_parallel']==True:
                self.args['tr_parallel']==False 
                print('Using CPU -> tr_parallel set to False')

    def _saveResults(self, model, model_args, opt, epoch, loss, ep_runtime, r, db_results, best):
        '''
        Save model/results in dictionary and write results csv.
        ''' 
        if (self.args['tr_checkpoint'] == 'best_only'):
            filename = self.runname + '.tar'
        else:
            filename = self.runname + '__' + ('ep_{:03d}'.format(epoch+1)) + '.tar'
        run_output_dir = os.path.join(self.args['output_dir'], self.runname)
        model_path = os.path.join(run_output_dir, filename)
        results_path = os.path.join(run_output_dir, self.runname+'__results.csv')
        Path(run_output_dir).mkdir(parents=True, exist_ok=True)              
        
        results = {
            'runname': self.runname,
            'epoch': '{:05d}'.format(epoch+1),
            'filename': filename,
            'loss': loss,
            'ep_runtime': '{:0.2f}'.format(ep_runtime),
            **self.runinfos,
            **r,
            **db_results,
            **self.args,
            }
        
        for key in results: 
            results[key] = str(results[key])                        

        if epoch==0:
            self.results_hist = pd.DataFrame(results, index=[0])
        else:
            self.results_hist.loc[epoch] = results
        self.results_hist.to_csv(results_path, index=False)


        if (self.args['tr_checkpoint'] == 'every_epoch') or (self.args['tr_checkpoint'] == 'best_only' and best):
      
            if hasattr(model, 'module'):
                state_dict = model.module.state_dict()
                model_name = model.module.name
            else:
                state_dict = model.state_dict()
                model_name = model.name
    
            torch_dict = {
                'runname': self.runname,
                'epoch': epoch+1,
                'model_args': model_args,
                'args': self.args,
                'model_state_dict': state_dict,
                'optimizer_state_dict': opt.state_dict(),
                'db_results': db_results,
                'results': results,
                'model_name': model_name,
                }
            
            torch.save(torch_dict, model_path)
            
        elif (self.args['tr_checkpoint']!='every_epoch') and (self.args['tr_checkpoint']!='best_only'):
            raise ValueError('selected tr_checkpoint option not available')
    
    def _saveResults_multi(self, model_1, model_2, model_3, model_args, opt, epoch, loss, ep_runtime, r, db_results, best):
        '''
        Save model/results in dictionary and write results csv.
        ''' 
        if (self.args['tr_checkpoint'] == 'best_only'):
            filename_1 = self.runname + '_1.tar'
            filename_2 = self.runname + '_2.tar'
            filename_3 = self.runname + '_3.tar'
        else:
            filename_1 = self.runname + '__' + ('ep_{:03d}'.format(epoch+1)) + '_1.tar'
            filename_2 = self.runname + '__' + ('ep_{:03d}'.format(epoch+1)) + '_2.tar'
            filename_3 = self.runname + '__' + ('ep_{:03d}'.format(epoch+1)) + '_3.tar'
        run_output_dir = os.path.join(self.args['output_dir'], self.runname)
        model_path_1 = os.path.join(run_output_dir, filename_1)
        model_path_2 = os.path.join(run_output_dir, filename_2)
        model_path_3 = os.path.join(run_output_dir, filename_3)
        results_path = os.path.join(run_output_dir, self.runname+'__results.csv')
        Path(run_output_dir).mkdir(parents=True, exist_ok=True)              
        
        results = {
            'runname': self.runname,
            'epoch': '{:05d}'.format(epoch+1),
            'filename': filename_1,
            'loss': loss,
            'ep_runtime': '{:0.2f}'.format(ep_runtime),
            **self.runinfos,
            **r,
            **db_results,
            **self.args,
            }
        
        for key in results: 
            results[key] = str(results[key])                        

        if epoch==0:
            self.results_hist = pd.DataFrame(results, index=[0])
        else:
            self.results_hist.loc[epoch] = results
        self.results_hist.to_csv(results_path, index=False)


        if (self.args['tr_checkpoint'] == 'every_epoch') or (self.args['tr_checkpoint'] == 'best_only' and best):
      
            if hasattr(model_1, 'module'):
                state_dict = model_1.module.state_dict()
                model_name = model_1.module.name
            else:
                state_dict = model_1.state_dict()
                model_name = model_1.name
    
            torch_dict = {
                'runname': self.runname,
                'epoch': epoch+1,
                'model_args': model_args,
                'args': self.args,
                'model_state_dict': state_dict,
                'optimizer_state_dict': opt.state_dict(),
                'db_results': db_results,
                'results': results,
                'model_name': model_name,
                }
            
            torch.save(torch_dict, model_path_1)
            
            if hasattr(model_2, 'module'):
                state_dict = model_2.module.state_dict()
                model_name = model_2.module.name
            else:
                state_dict = model_2.state_dict()
                model_name = model_2.name
    
            torch_dict = {
                'runname': self.runname,
                'epoch': epoch+1,
                'model_args': model_args,
                'args': self.args,
                'model_state_dict': state_dict,
                'optimizer_state_dict': opt.state_dict(),
                'db_results': db_results,
                'results': results,
                'model_name': model_name,
                }
            
            torch.save(torch_dict, model_path_2)
            
            if hasattr(model_3, 'module'):
                state_dict = model_3.module.state_dict()
                model_name = model_3.module.name
            else:
                state_dict = model_3.state_dict()
                model_name = model_3.name
    
            torch_dict = {
                'runname': self.runname,
                'epoch': epoch+1,
                'model_args': model_args,
                'args': self.args,
                'model_state_dict': state_dict,
                'optimizer_state_dict': opt.state_dict(),
                'db_results': db_results,
                'results': results,
                'model_name': model_name,
                }
            
            torch.save(torch_dict, model_path_3)
            
        elif (self.args['tr_checkpoint']!='every_epoch') and (self.args['tr_checkpoint']!='best_only'):
            raise ValueError('selected tr_checkpoint option not available')

            
