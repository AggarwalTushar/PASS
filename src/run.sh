MODEL=""
DATA_DIR="data"
INPUT_FILE="input.txt"
AUDIENCE_TYPE="technical


# Extract text and images from the input file
python text_and_image_extractor.py --input_file $INPUT_FILE --data_dir $DATA_DIR


# To generate the slides
if [[ "$model_name" == "gpt-4o" ]]; then
    python src/slide_generation_gpt.py --type "title_generator" --data_dir $DATA_DIR --MODEL $MODEL --audience_type $AUDIENCE_TYPE 
    python src/slide_generation_gpt.py --type "content_extractor" --data_dir $DATA_DIR --MODEL $MODEL --audience_type $AUDIENCE_TYPE 
    python src/slide_generation_gpt.py --type "summarizer" --data_dir $DATA_DIR --MODEL $MODEL --audience_type $AUDIENCE_TYPE 
else
    python src/slide_generation.py --type "title_generator" --data_dir $DATA_DIR --MODEL $MODEL --audience_type $AUDIENCE_TYPE 
    python src/slide_generation.py --type "content_extractor" --data_dir $DATA_DIR --MODEL $MODEL --audience_type $AUDIENCE_TYPE 
    python src/slide_generation.py --type "summarizer" --data_dir $DATA_DIR --MODEL $MODEL --audience_type $AUDIENCE_TYPE 
fi

# To map the images to the slides
python src/image_mapping.py --data_dir $DATA_DIR --MODEL $MODEL --audience_type $AUDIENCE_TYPE


