def get_entities_withtags(tokens, tags):
    """
    Input : 
        Tokens => ["w1", "w2", "w3", "w4", "w5"]
        Tags =>  ["B-ORG", "O", "B-LOC","I-LOC", "O"]

        
    Return entity texts -> ["w1", "w3 w4"] with ["ORG", "LOC"]
    """
    bucket = []
    tags_bucket = []
    
    tok_idx = []
    
    merged_tokens = []
    merged_tags = []
    merged_tok_idces = []
    
    prevtag = ''
    for idx, (tok, tag) in enumerate(zip(tokens,tags)):
        if tag == "O" and len(bucket) != 0:
            merged_tokens.append(" ".join(bucket))
            merged_tags.append(prevtag)
            merged_tok_idces.append(tok_idx)
            bucket = []
            tok_idx = []
        
        elif tag == "O" and len(bucket) == 0:
            bucket = []
            tok_idx = []
            
        elif tag.startswith("I-"):
            bucket.append(tok)
            tok_idx.append(idx)

        elif tag.startswith("B") and len(bucket) != 0:
            merged_tokens.append(" ".join(bucket))
            merged_tags.append(prevtag)
            bucket = []
            bucket.append(tok)
            tok_idx = []
            tok_idx.append(idx)

        elif tag.startswith("B") and len(bucket) == 0:
            bucket.append(tok)
            tok_idx.append(idx)
        
        prevtag = tag[2:]

    if len(bucket)!=0: 
        merged_tokens.append((" ").join(bucket))
        merged_tags.append(prevtag)
        merged_tok_idces.append(tok_idx)

    return merged_tokens, merged_tags, merged_tok_idces


def get_entities(list_of_tags):
    """
    Input : 
        Tags =>  [["B-ORG", "O", "B-LOC","I-LOC", "O"],
                 ["B-ORG", "O", "B-LOC","I-LOC", "O"]]

        
    Return entity texts -> ["w1", "w3 w4"] with ["ORG", "LOC"]
    """
    list_of_merged_tags = []
    for tags in list_of_tags:
        bucket = []    
        merged_tags = []
        
        prevtag = ''
        for idx, tag in enumerate(tags):
            if tag == "O" and len(bucket) != 0:
                merged_tags.append(prevtag)
                bucket = []
        
            
            elif tag == "O" and len(bucket) == 0:
                bucket = []
        
                
            elif tag.startswith("I-"):
                bucket.append(tag)

            elif tag.startswith("B") and len(bucket) != 0:
                merged_tags.append(prevtag)
                bucket = []
                bucket.append(tag)

            elif tag.startswith("B") and len(bucket) == 0:
                bucket.append(tag)
            
            prevtag = tag[2:]

        if len(bucket)!=0: 
            merged_tags.append(prevtag)

        list_of_merged_tags.append(merged_tags)

    return list_of_merged_tags
