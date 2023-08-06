
import os
import csv
import sys
import collections

# import shap
# import joblib
import xgboost

import numpy as np # downloaded as shap dependency as many other things

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import  accuracy_score, plot_confusion_matrix

# from shap.plots._beeswarm import summary_legacy
# """
# 1,2
# 1,3
# 2,3
# """

class Post_ggi:

    def __init__(self, 
                 feature_file = None,
                 all_ggi_results = None,
                 file_comparisons = None,
                 model_prefix = "post_ggi",
                 max_display = 17,
                 cnfx_ncols = 3,
                 threads = 1
                 ) -> None:

        self.feature_file = feature_file
        self.all_ggi_results = all_ggi_results
        self.file_comparisons = file_comparisons

        self.model_prefix = model_prefix
        self.cnf_ncols = cnfx_ncols
        self.threads = threads

        self.drop_columns = [
            'Group', 'aln_base', 
            'SymPval', 'MarPval', 
            'IntPval'
        ]

        # self.metadata_columns = [
        #     'model_filename',
        #     'accuracy',
        #     'pos_hypo',
        #     'neg_hypo'
        # ]

        self.metadata_columns = [
            'pos_hypo',
            'neg_hypo',
            'accuracy',
        ]

        self.max_display = max_display

        # previously tuned hyperparameters
        self.gamma = 0.14210526315789473
        self.learning_rate = 0.03
        self.max_depth = 4
        self.reg_lambda = 0.018
        self.n_estimators = 4200

    @property    
    def ggi_df(self):

        if not self.all_ggi_results:
            return None

        ggi_rows = []
        with open(self.all_ggi_results, 'r') as f:
            reader = csv.reader(f, delimiter = '\t')
            for row in reader:
                ggi_rows.append(row)

        return ggi_rows

    @property
    def tree_id_comp(self):

        if not self.file_comparisons:
            return None

        tree_id_comp = []
        with open(self.file_comparisons, 'r') as f:
            reader = csv.reader(f, delimiter = ',')
            for row in reader:
                tree_id_comp.append(row)

        return tree_id_comp

    @property
    def features(self):
        return pd.read_csv(self.feature_file, sep = '\t')

    def subset_tree_id(self, tree_id_comp1):
        """
        subset tree_id_comp df
        by a tree_id
        """
        ha,hb = tree_id_comp1

        if not self.ggi_df:
            return None

        subset_df = []
        for row in self.ggi_df:

            rank = row[3]
            if rank != '1':
                continue

            aln_base = row[0]
            tree_id  = row[1]

            # contained = set(tree_id_comp1) & set([tree_id])

            if tree_id == ha or tree_id == hb:
                subset_df.append([aln_base, tree_id])

        if not subset_df:
            sys.stderr.write("Tree ids '%s' do not match with\n" % ", ".join(tree_id_comp1))
            sys.stderr.write("'%s' data frame\n" % self.all_ggi_results)
            sys.stderr.flush()
            return None

        return pd.DataFrame(subset_df, columns = ['alignment', 'hypothesis'])
        
    def make_specific_prefix(self, tree_id_comp1):
        return "%s_h%s_h%s" % (self.model_prefix, tree_id_comp1[0], tree_id_comp1[1])

    def _bar_data(self, shap_values, all_num):

        max_display = self.max_display
        shap_means  = np.abs(shap_values).mean(0)
        mysort      = np.argsort(shap_means)[::-1]
        
        y_axis = all_num.columns[mysort][:max_display][::-1]
        x_axis = shap_means[mysort][:max_display][::-1]

        return y_axis, x_axis

    def _my_dependency_plot(self, all_num, lead, shap_values):

        from shap.plots._scatter import dependence_legacy
        import numpy as np
        import matplotlib.colors as mcolors
        from matplotlib import cm


        tra = shap_values.values.T

        lead = 'supp_mean'
        # layer = 'supp_mean'
        for layer in all_num.columns:

            if layer == lead:
                continue

            ind = np.argwhere( all_num.columns == lead  ).flatten()[0]
            interaction_index = np.argwhere( all_num.columns == layer  ).flatten()[0]

            covar = all_num.iloc[:,interaction_index]
            pre_cmap = cm.get_cmap('viridis', len(covar))

            hexes = [ mcolors.rgb2hex( pre_cmap(i)  ) for i in range(len(covar)) ]
            cmap,norm = mcolors.from_levels_and_colors(sorted([0]+list(covar)), hexes)

            plt.scatter(
                all_num.iloc[:,ind],
                tra[ind,:],
                c = list(covar),
                cmap = cmap,
                norm = norm,
                s = 19, alpha = 0.9
            )
            plt.xlabel(lead)
            plt.ylabel('SHAP value')
            cbar = plt.colorbar( cm.ScalarMappable(norm = norm, cmap= cmap) )
            cbar.set_label(layer)
            
            plt.tight_layout(pad=0.05)
            plt.savefig("dependencies_plot/shap_%s_%s.png" % (lead,layer), dpi = 330)
            plt.close()

    def _update_meta_and_bardata(self, shap_values, accuracy, _groups_dict, all_num):
        """
        # update metadata & get bar data
        """
        # model_filename = '%s.sav' % new_prefix
        # self.add_metdata(
        #     self._join_shaps(shap_values, 
        #                      [ model_filename,
        #                        accuracy,
        #                        _groups_dict[True ],
        #                        _groups_dict[False]  ] ) )

        self.add_metdata(
            self._join_shaps(shap_values, 
                             [ _groups_dict[True ],
                               _groups_dict[False],
                               accuracy, ] ), 
            False
        )

        return self._bar_data( shap_values, all_num ) 

    def shap_things(self, xgb_clf_no_nor, all_num, new_prefix, _groups_dict, accuracy):
        
        # heavy imports
        from shap import Explainer
        from shap.plots._beeswarm import summary_legacy
        # heavy imports

        # xgb_clf_no_nor, all_num, new_prefix = xgb_clf_no_nor, all_num, new_prefix

        bee_20_filename = "best%s_beeswarm_%s.png" % (self.max_display,new_prefix)

        explainer     = Explainer(xgb_clf_no_nor, all_num)
        shap_values   = explainer(all_num)

        y_axis,x_axis = self._update_meta_and_bardata( shap_values.values, accuracy, 
                                                       _groups_dict, all_num )
        
        gs = gridspec.GridSpec(1, 2,  width_ratios=[1, 1.7]) 
        # plt.rcParams['font.size'] = 14.0

        plt.subplot( gs[0] )
        plt.barh(
            y_axis, x_axis, height=0.6,
            align  ='center',
            color  = 'gray',
            zorder = 3
        )
        plt.yticks([])
        plt.grid(True, which='major', axis='x')
        plt.gca().invert_xaxis()
        plt.xlabel('mean(|SHAP value|)', fontsize = 13)

        plt.subplot( gs[1] )
        summary_legacy(
            shap_values,
            max_display = self.max_display,
            plot_size   = (self.max_display*0.5, self.max_display*0.3),
            show = False
        )

        plt.title(_groups_dict[True], loc = 'right')
        plt.title(_groups_dict[False], loc = 'left')
        plt.tight_layout(pad=0.05)
        plt.savefig(bee_20_filename, dpi = 330)
        plt.close()

    def _join_shaps(self, shap_values, values):

        joined = []
        for row in shap_values:
            joined += [values + list(row)]

        return joined

    def _get_columns(self):
        cols = list(self.features.columns)

        for i in self.drop_columns:
            if cols.__contains__(i):
                cols.remove(i)

        return self.metadata_columns + cols

    def add_metdata(self, values, init):

        metadata_filename = '%s_metadata.tsv' % self.model_prefix

        if init:

            with open(metadata_filename, 'w') as f:
                writer = csv.writer(f, delimiter = "\t")
                writer.writerows( [self._get_columns()] )

        else:

            with open(metadata_filename, 'a') as f:
                writer = csv.writer(f, delimiter = "\t")
                writer.writerows(values)

        sys.stdout.write('\tWritting metadata at: "%s"\n\n' % metadata_filename)
        sys.stdout.flush()
        
    def xgboost_classifier(self, tree_id_comp1):

        # tree_id_comp1 = self.tree_id_comp[1]

        if not tree_id_comp1:
            return None

        dataset = "H%s-H%s" % tuple(tree_id_comp1)
        new_prefix = self.make_specific_prefix(tree_id_comp1)
        # model_filename = '%s.sav' % new_prefix

        sys.stdout.write('Processing: "%s" dataset\n' % dataset)
        sys.stdout.flush()

        features = self.features
        target = self.subset_tree_id(tree_id_comp1)

        # merge 
        aln_base,hypothesis = target.columns
        aln_feature = features.columns[0]

        target = target.rename({aln_base: aln_feature}, axis = 1)
        merged_dataset = features.merge(target, on = aln_feature, how='left')
        new_df = merged_dataset[merged_dataset[hypothesis].notna()].reset_index(drop=True)

        for c in self.drop_columns:
            try:
                new_df = new_df.drop( c, 1 )
            except KeyError:
                pass

        # hypotheses definition
        _groups_dict = { 
            True  : 'H%s' % tree_id_comp1[0],
            False : 'H%s' % tree_id_comp1[1]
        }

        split = StratifiedShuffleSplit(n_splits = 1, test_size = 0.25, random_state = 42)
        for train_index, _ in split.split(new_df, new_df[hypothesis]):
            strat_train_set = new_df.loc[train_index]
            # strat_test_set  = new_df.loc[test_index]
        
        train_num = strat_train_set.drop(hypothesis, axis=1)
        train_labels = strat_train_set[hypothesis] == tree_id_comp1[0]
    
        all_num  = new_df.drop(hypothesis, axis=1)
        all_labels = new_df[hypothesis] == tree_id_comp1[0]

        fr_tr = collections.Counter(all_labels)

        if len(fr_tr) <= 1:
            sys.stdout.write("Less than two labels found in the '%s' dataset\n" % dataset)
            sys.stdout.flush()
            return None
        
        scale_pos_weight = fr_tr[False]/fr_tr[True]

        xgb_clf_no_nor = xgboost.XGBClassifier(
                            objective = 'binary:logistic',
                            colsample_bytree = 0.5,
                            subsample = 0.9,

                            use_label_encoder = not True,
                            scale_pos_weight = scale_pos_weight,
                            
                            gamma = self.gamma,
                            learning_rate = self.learning_rate,
                            max_depth = self.max_depth,
                            reg_lambda = self.reg_lambda,
                            n_estimators = self.n_estimators,

                            n_jobs = self.threads
                        )

        sys.stdout.write("\tRunning the XGBoost classifier\r")
        sys.stdout.flush()

        xgb_clf_no_nor.fit(all_num, all_labels.tolist(),
                           eval_set = [ (train_num, train_labels.tolist()) ],
                           early_stopping_rounds = 2000,
                           verbose = False,
                           eval_metric = 'aucpr'
                        )

        accuracy = accuracy_score(all_labels, xgb_clf_no_nor.predict(all_num))

        sys.stdout.write("\tRunning the XGBoost classifier, overall accuracy: %s\n" % round(accuracy, 6))
        sys.stdout.flush()

        sys.stdout.write("\tCalculating SHAP values\n")
        sys.stdout.flush()

        self.shap_things(
            xgb_clf_no_nor,
            all_num, 
            new_prefix, 
            _groups_dict, 
            accuracy
        )

        # joblib.dump(xgb_clf_no_nor, model_filename)
        return (all_num, all_labels, 
                _groups_dict, xgb_clf_no_nor, 
                dataset)

    def confusion_plots(self, mytables):

        if not mytables:
            return None

        cnf_mx_filename = "cnf_mx_%s.png" % self.model_prefix

        if len(self.tree_id_comp)  <= 1:

            X, y,_groups_dict,xgb_clf_no_nor,title = mytables[0]
            plot_confusion_matrix(
                xgb_clf_no_nor, X, y,
                values_format  = 'd',
                display_labels = [_groups_dict[i] for i in xgb_clf_no_nor.classes_]
            )
            # axes[i].set_title(title, fontsize = 20)
            plt.savefig(cnf_mx_filename, bbox_inches = 'tight')
            plt.close()
            

        else: 
            if len(self.tree_id_comp) <= 3:
                nrows = 1
                self.cnf_ncols = len(self.tree_id_comp)
                
            else:
                res = len(mytables) % self.cnf_ncols
                nrows = (len(mytables) // self.cnf_ncols) + bool(res)

            f,axes = plt.subplots(nrows = nrows, ncols = self.cnf_ncols, figsize=(18, 5), dpi = 400)
            for i in range(len(mytables)):
                X, y,_groups_dict,xgb_clf_no_nor,title = mytables[i]

                plot_confusion_matrix(
                    xgb_clf_no_nor, X, y,
                    values_format  = 'd',
                    display_labels = [_groups_dict[i] for i in xgb_clf_no_nor.classes_],
                    ax = axes[i]
                )
                axes[i].set_title(title, fontsize = 20)

            plt.savefig(cnf_mx_filename, bbox_inches = 'tight')
            plt.close()

    def xgboost_iterator(self):

        self.add_metdata(None,  True)        

        mytables = []
        for tree_id_comp1 in self.tree_id_comp:

            tmp_model = self.xgboost_classifier(tree_id_comp1)
            if tmp_model:
                mytables.append(tmp_model)

        sys.stdout.write("Plotting confusion matrices\n")
        sys.stdout.flush()

        self.confusion_plots(mytables)

# debugging --------------------------------------

# import os
# base_path = '/Users/ulises/Desktop/GOL/software/GGpy/proofs_ggi/postRaxmlBug/flatfishes'

# file_comparisons = os.path.join(base_path, 'comparisonfile.txt')
# # features_file    = '/Users/ulises/Desktop/ABL/GGI_flatfishes/post_ggi/features_fstats_yongxin.tsv'
# features_file    = os.path.join(base_path, 'features_991exons_fishlife.tsv')
# all_ggi_results  = os.path.join(base_path, 'raxml_noRaxmlBug_results_clean_ggi.tsv')
# threads = 5

# self = Post_ggi(
#     feature_file = features_file,
#     all_ggi_results = all_ggi_results,
#     file_comparisons = file_comparisons,
#     threads = 6
# )
# self.xgboost_classifier(self.tree_id_comp[1])

# debugging --------------------------------------
