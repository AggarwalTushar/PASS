MODEL=""
DATA_DIR="data"
INPUT_FILE="input.txt"
AUDIENCE_TYPE="technical"


# Extract text and images from the input file
python src/text_and_image_extractor.py --input_file $INPUT_FILE --output_dir $DATA_DIR


# To generate the slides
if [[ "$MODEL" == "gpt-4o" ]]; then
    python src/slide_generation_gpt.py --type "title_generator" --data_dir $DATA_DIR --model $MODEL --audience_type $AUDIENCE_TYPE 
    python src/slide_generation_gpt.py --type "content_extractor" --data_dir $DATA_DIR --model $MODEL --audience_type $AUDIENCE_TYPE 
    python src/slide_generation_gpt.py --type "summarizer" --data_dir $DATA_DIR --model $MODEL --audience_type $AUDIENCE_TYPE 
else
    python src/slide_generation_llm.py --type "title_generator" --data_dir $DATA_DIR --model $MODEL --audience_type $AUDIENCE_TYPE 
    python src/slide_generation_llm.py --type "content_extractor" --data_dir $DATA_DIR --model $MODEL --audience_type $AUDIENCE_TYPE 
    python src/slide_generation_llm.py --type "summarizer" --data_dir $DATA_DIR --model $MODEL --audience_type $AUDIENCE_TYPE 
fi

# To map the images to the slides
python src/image_mapper.py --data_dir $DATA_DIR --model $MODEL --audience_type $AUDIENCE_TYPE


