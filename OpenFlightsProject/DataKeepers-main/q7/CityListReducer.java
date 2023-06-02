import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.conf.Configuration;
import java.io.IOException;
import java.nio.file.AccessDeniedException;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Reducer.Context;
import java.util.Iterator;
import java.util.ArrayList;

public class CityListReducer extends Reducer<Text, Text, Text, Text>  
{
    private Text empty = new Text();
    private Text v = new Text();

    @Override
    public void reduce(Text key, Iterable<Text> values, Context context)
        throws IOException, InterruptedException
    {
        String combined = "";
        int i = 0;
        for(Text value : values)
        {
            i++;
            combined = combined + value.toString() + " ";
        }


        combined = combined.strip();
        if (i > 1)
        {
            // add parenthesis since has spaces
            combined = "\"" + combined + "\"";
        }
        
        v.set(combined);
        context.write(empty, v);
    }
}