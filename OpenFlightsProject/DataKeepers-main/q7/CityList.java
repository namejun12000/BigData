import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.fs.Path;

public class CityList
{
    public static void main(String[] args) throws Exception
    {
        Configuration conf = new Configuration();
        conf.set("TargetCity1", args[0]);
        conf.set("TargetCity2", args[1]);
        Job job = Job.getInstance(conf, "CityList");
        job.setJarByClass(CityList.class);
        job.setMapperClass(CityListMapper.class);
        job.setReducerClass(CityListReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        FileInputFormat.addInputPath(job, new Path("airports"));
        FileOutputFormat.setOutputPath(job, new Path("output"));
        job.waitForCompletion(true);
    }
}