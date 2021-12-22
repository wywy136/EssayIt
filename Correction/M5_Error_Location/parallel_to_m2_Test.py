import argparse
import os
import spacy
from contextlib import ExitStack
from nltk.stem.lancaster import LancasterStemmer
import sys
sys.path.append('/root/code_5000/wy/Correction/M5_Error_Location/scripts/')
#import scripts.align_text as align_text
#import scripts.cat_rules as cat_rules
#import scripts.toolbox as toolbox
import align_text
import cat_rules
import toolbox



def main(Spell_corrected_context, Grammar_corrected_context, M5):
    # Get base working directory.

    lang = M5[0]
    stemmer = M5[1]
    gb_spell = M5[2]
    tag_map = M5[3]

    print("Loading resources...")

    # Load Tokenizer and other resources

    # Setup output m2 file
    # out_m2 = open(args.out, "w")
    # 10.22:
    out_m2 = []

    # ExitStack lets us process an arbitrary number of files line by line simultaneously.
    # See https://stackoverflow.com/questions/24108769/how-to-read-and-process-multiple-files-simultaneously-in-python
    print("Processing files...")
    # Process each line of all input files.
    for line_orig, line_cor in zip(Spell_corrected_context, Grammar_corrected_context):
        orig_sent = line_orig
        cor_sents = (line_cor + "\n",)
        # If orig sent is empty, skip the line
        if not orig_sent: continue
        # Write the original sentence to the output m2 file.
        out_m2.append("S "+orig_sent)
        # out_m2.append("\n")
        # Markup the original sentence with spacy (assume tokenized)
        proc_orig = toolbox.applySpacy(orig_sent.split(), lang)
        # Loop through the corrected sentences
        for cor_id, cor_sent in enumerate(cor_sents):
            cor_sent = cor_sent.strip()
            # Identical sentences have no edits, so just write noop.
            if orig_sent == cor_sent:
                out_m2.append("A -1 -1|||noop|||-NONE-|||REQUIRED|||-NONE-|||"+str(cor_id))
                # out_m2.append("\n")
            # Otherwise, do extra processing.
            else:
                # Markup the corrected sentence with spacy (assume tokenized)
                proc_cor = toolbox.applySpacy(cor_sent.strip().split(), lang)
                # Auto align the parallel sentences and extract the edits.
                auto_edits = align_text.getAutoAlignedEdits(proc_orig, proc_cor, lang, False, "rules")
                # Loop through the edits.
                for auto_edit in auto_edits:
                    # Give each edit an automatic error type.
                    cat = cat_rules.autoTypeEdit(auto_edit, proc_orig, proc_cor, gb_spell, tag_map, lang, stemmer)
                    auto_edit[2] = cat
                    # Write the edit to the output m2 file.
                    out_m2.append(toolbox.formatEdit(auto_edit, cor_id))
                    # out_m2.append("\n")
        # Write a newline when we have processed all corrections for a given sentence.
        out_m2.append("\n")

    return out_m2

# if __name__ == "__main__":
#     # Define and parse program input
#     parser = argparse.ArgumentParser(description="Convert parallel original and corrected text files (1 sentence per line) into M2 format.\nThe default uses Damerau-Levenshtein and merging rules and assumes tokenized text.",
#                                 formatter_class=argparse.RawTextHelpFormatter,
#                                 usage="%(prog)s [-h] [options] -orig ORIG -cor COR [COR ...] -out OUT")
#     parser.add_argument("-orig", help="The path to the original text file.", required=True)
#     parser.add_argument("-cor", help="The paths to >= 1 corrected text files.", nargs="+", default=[], required=True)
#     parser.add_argument("-out", help="The output filepath.", required=True)
#     parser.add_argument("-lev", help="Use standard Levenshtein to align sentences.", action="store_true")
#     parser.add_argument("-merge", choices=["rules", "all-split", "all-merge", "all-equal"], default="rules",
#                         help="Choose a merging strategy for automatic alignment.\n"
#                             "rules: Use a rule-based merging strategy (default)\n"
#                             "all-split: Merge nothing; e.g. MSSDI -> M, S, S, D, I\n"
#                             "all-merge: Merge adjacent non-matches; e.g. MSSDI -> M, SSDI\n"
#                             "all-equal: Merge adjacent same-type non-matches; e.g. MSSDI -> M, SS, D, I")
#     args = parser.parse_args()
#     # Run the program.
#     main(args)
