echo "Preparing for running code ........."
echo ""
echo "Creating the output directory....."
if [ ! -d "./output" ]; then
  mkdir output
fi

echo "Creating the plot directory....."
if [ ! -d "./plots/" ]; then
  mkdir -p "./plots"
fi

echo ""
echo "Finished preparations."
echo ""

echo "Executing code ........."
echo "Executing assignment-1.a.........."
python3 ./code/assignment1_a.py > ./output/assignment1_a_out.txt

echo "Executing assignment-1.b.........."
python3 ./code/assignment1_b.py > ./output/assignment1_b_out.txt

echo "Executing assignment-2.a.........."
python3 ./code/assignment2_a.py > ./output/assignment2_a_out.txt

echo "Executing assignment-2.b.........."
python3 ./code/assignment2_b.py > ./output/assignment2_b_out.txt

echo "Executing assignment-2.c.........."
python3 ./code/assignment2_c.py > ./output/assignment2_c_out.txt

echo "Executing assignment-2.d.........."
python3 ./code/assignment2_d.py > ./output/assignment2_d_out.txt

echo "Executing assignment-2.e.........."
python3 ./code/assignment2_e.py > ./output/assignment2_e_out.txt

echo "Executing assignment-2.f.........."
python3 ./code/assignment2_f.py > ./output/assignment2_f_out.txt

echo "Executing assignment-2.g.........."
python3 ./code/assignment2_g.py > ./output/assignment2_g_out.txt

echo "Executing assignment-2.h.........."
python3 ./code/assignment2_h.py > ./output/assignment2_h_out.txt

echo "Executing assignment-3.a.........."
python3 ./code/assignment3_a.py > ./output/assignment3_a_out.txt



