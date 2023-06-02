import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.conf.Configuration;
import java.io.IOException;
import java.nio.file.AccessDeniedException;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Reducer.Context;
import java.util.Iterator;
import java.util.ArrayList;

public class QSevenReducer4 extends Reducer<Text, Text, Text, Text>  
{
    private int round;
    private Text val = new Text();
    private Text empty = new Text();

    public void setup(Context context)
    {
        Configuration conf = context.getConfiguration();
        round = Integer.parseInt(conf.get("round"));
    }

    @Override
    public void reduce(Text key, Iterable<Text> values, Context context)
        throws IOException, InterruptedException
    {
        if (key.toString().equals("translated"))
        {
            for(Text value : values)
            {
                context.write(empty, value);
            }
        }
        else
        {
            // search for record in order to translate
            // while searching for record, add paths to a list
            ArrayList<String> paths = new ArrayList<String>();
            String record = "";

            Iterator<org.apache.hadoop.io.Text> valuesIt = values.iterator();
            while (valuesIt.hasNext())
            {
                String value = valuesIt.next().toString().trim();
                if (value.contains(","))
                {
                    // record
                    record = value;
                    break;
                }
                
                paths.add(value);
            }

            // get name of airport / airline
            String name = record.split(",")[1];
            name = name.replaceAll("\\s+", "_");

            // translate paths
            for(String path : paths)
            {
                String[] p = path.split("\\s+");
                p[round - 1] = name;

                // convert p to string and write
                String result = "";
                for (int i = 0; i < p.length; i++)
                {
                    result = result  + p[i] + " ";
                }
                result = result.trim();
                val.set(result);
                context.write(empty, val);
            }

            // translate rest of paths in valuesIt
            while(valuesIt.hasNext())
            {
                String path = valuesIt.next().toString().trim();
                String[] p = path.split("\\s+");
                p[round - 1] = name;

                // convert p to string and write
                String result = "";
                for (int i = 0; i < p.length; i++)
                {
                    result = result  + p[i] + " ";
                }
                result = result.trim();
                val.set(result);
                context.write(empty, val);
            }
        }
    }
}