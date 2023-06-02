import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.conf.Configuration;
import java.io.IOException;
import java.nio.file.AccessDeniedException;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Reducer.Context;
import java.util.Iterator;

public class QOneReducer extends Reducer<Text, Text, Text, Text>  
{
    private String targetCountry;

    public void setup(Context context)
    {
        Configuration conf = context.getConfiguration();
        targetCountry = conf.get("Country");
    }

    @Override
    public void reduce(Text key, Iterable<Text> values, Context context)
        throws IOException, InterruptedException
    {
        String country = key.toString().trim();
        if (country.equals(targetCountry))
        {
            for(Text value : values)
            {
                context.write(key, value);
            }
        }
    }
}