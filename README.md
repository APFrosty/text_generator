# TODO
[TODO.md](https://github.com/APFrosty/text_generator/blob/master/TODO.md)

# Generate n-gram language model

Syntax : 
```/model_generator.py <input_dir> <n> <output_model>```

Example :
```console
user@host:~/text_generator$ model_generator/model_generator.py corpus/W 3 W_3.model
Processing file corpus/W/Waliszewski,_Kazimierz-Le_roman_d_une_imperatrice.pdf.seg... 1.317619MB
Processing file corpus/W/Wallace,_Edgar-Dan_le_sosie.pdf.seg... 1.676214MB
...
Processing file corpus/W/Wilde,_Oscar-Le_portrait_de_Dorian_Gray.pdf.seg... 5.585237MB
Processing file corpus/W/Woolf,_Virginia-Orlando.pdf.seg... 6.109955MB
Sorting frequency map... DONE
Calculating frequency map... DONE
Took 8.527957916259766 seconds
```

Then the output_model file is created.

# Generate an n-length sentence based on a language model

Syntax : 
```/based_on_lang_model.py <model_file> <n>```

Example :
```console
user@host:~/text_generator$ sentence_generator/based_on_lang_model.py W_3.model 10
['reportez', 'lui', 'le', 'roman', 'd’une', 'impératrice', 'chapitre', 'iii', 'de', 'la']
```

# Generate sentences from templates based on neuronal model embeddings

Example :
```console
user@host:~/text_generator/neuronal$ generator.py
~ tristesse ~
Il n' y a pas_de tristesse sans navrement .
Il n' y a ni exultante ni tristesse en mélancolie .

...

~ bleu ~
Il n' y a pas_de bleue sans bleu .
Il n' y a ni bleue ni scabieuse en bouffette .
En bleue , la gazouillante scabieuse roussit la plus incarnadine
La bleue roussit une scabieuse .
L' outremer de les cannetilles roussit à la bleue ce_que la scabieuse roussit à l' orangé .
Les gris de cannetilles constellent de la bleue ce_que les burnouss constellent de l' outremer .
```
