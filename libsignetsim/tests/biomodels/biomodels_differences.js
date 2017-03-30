var list_ids = ['BIOMD0000000001', 'BIOMD0000000002', 'BIOMD0000000003', 'BIOMD0000000004', 'BIOMD0000000005',
	'BIOMD0000000006', 'BIOMD0000000007', 'BIOMD0000000008', 'BIOMD0000000009', 'BIOMD0000000010',
	'BIOMD0000000011', 'BIOMD0000000012', 'BIOMD0000000013', 'BIOMD0000000014', 'BIOMD0000000015',
	'BIOMD0000000016', 'BIOMD0000000017', 'BIOMD0000000018', 'BIOMD0000000019', 'BIOMD0000000020',
	'BIOMD0000000021', 'BIOMD0000000022', 'BIOMD0000000023', 'BIOMD0000000024', 'BIOMD0000000025',
	'BIOMD0000000026', 'BIOMD0000000027', 'BIOMD0000000028', 'BIOMD0000000029', 'BIOMD0000000030',
	'BIOMD0000000031', 'BIOMD0000000032', 'BIOMD0000000033', 'BIOMD0000000034', 'BIOMD0000000035',
	'BIOMD0000000036', 'BIOMD0000000037', 'BIOMD0000000038', 'BIOMD0000000039', 'BIOMD0000000040',
	'BIOMD0000000041', 'BIOMD0000000042', 'BIOMD0000000043', 'BIOMD0000000044', 'BIOMD0000000045',
	'BIOMD0000000046', 'BIOMD0000000047', 'BIOMD0000000048', 'BIOMD0000000049', 'BIOMD0000000050',
	'BIOMD0000000051', 'BIOMD0000000052', 'BIOMD0000000053', 'BIOMD0000000054', 'BIOMD0000000055',
	'BIOMD0000000056', 'BIOMD0000000057', 'BIOMD0000000058', 'BIOMD0000000059', 'BIOMD0000000060',
	'BIOMD0000000061', 'BIOMD0000000062', 'BIOMD0000000063', 'BIOMD0000000064', 'BIOMD0000000065',
	'BIOMD0000000066', 'BIOMD0000000067', 'BIOMD0000000068', 'BIOMD0000000069', 'BIOMD0000000070',
	'BIOMD0000000071', 'BIOMD0000000072', 'BIOMD0000000073', 'BIOMD0000000074', 'BIOMD0000000075',
	'BIOMD0000000076', 'BIOMD0000000077', 'BIOMD0000000078', 'BIOMD0000000079', 'BIOMD0000000080',
	'BIOMD0000000081', 'BIOMD0000000082', 'BIOMD0000000083', 'BIOMD0000000084', 'BIOMD0000000085',
	'BIOMD0000000086', 'BIOMD0000000087', 'BIOMD0000000088', 'BIOMD0000000089', 'BIOMD0000000090',
	'BIOMD0000000091', 'BIOMD0000000092', 'BIOMD0000000093', 'BIOMD0000000094', 'BIOMD0000000095',
	'BIOMD0000000096', 'BIOMD0000000097', 'BIOMD0000000098', 'BIOMD0000000099', 'BIOMD0000000100',
	'BIOMD0000000101', 'BIOMD0000000102', 'BIOMD0000000103', 'BIOMD0000000104', 'BIOMD0000000105',
	'BIOMD0000000106', 'BIOMD0000000107', 'BIOMD0000000108', 'BIOMD0000000109', 'BIOMD0000000110',
	'BIOMD0000000111', 'BIOMD0000000112', 'BIOMD0000000113', 'BIOMD0000000114', 'BIOMD0000000115',
	'BIOMD0000000116', 'BIOMD0000000117', 'BIOMD0000000118', 'BIOMD0000000119', 'BIOMD0000000120',
	'BIOMD0000000121', 'BIOMD0000000122', 'BIOMD0000000123', 'BIOMD0000000124', 'BIOMD0000000125',
	'BIOMD0000000126', 'BIOMD0000000127', 'BIOMD0000000128', 'BIOMD0000000129', 'BIOMD0000000130',
	'BIOMD0000000131', 'BIOMD0000000132', 'BIOMD0000000133', 'BIOMD0000000134', 'BIOMD0000000135',
	'BIOMD0000000136', 'BIOMD0000000137', 'BIOMD0000000138', 'BIOMD0000000139', 'BIOMD0000000140',
	'BIOMD0000000141', 'BIOMD0000000142', 'BIOMD0000000143', 'BIOMD0000000144', 'BIOMD0000000145',
	'BIOMD0000000146', 'BIOMD0000000147', 'BIOMD0000000148', 'BIOMD0000000149', 'BIOMD0000000150',
	'BIOMD0000000151', 'BIOMD0000000152', 'BIOMD0000000153', 'BIOMD0000000154', 'BIOMD0000000155',
	'BIOMD0000000156', 'BIOMD0000000157', 'BIOMD0000000158', 'BIOMD0000000159', 'BIOMD0000000160',
	'BIOMD0000000161', 'BIOMD0000000162', 'BIOMD0000000163', 'BIOMD0000000164', 'BIOMD0000000165',
	'BIOMD0000000166', 'BIOMD0000000167', 'BIOMD0000000168', 'BIOMD0000000169', 'BIOMD0000000170',
	'BIOMD0000000171', 'BIOMD0000000172', 'BIOMD0000000173', 'BIOMD0000000174', 'BIOMD0000000175',
	'BIOMD0000000176', 'BIOMD0000000177', 'BIOMD0000000178', 'BIOMD0000000179', 'BIOMD0000000180',
	'BIOMD0000000181', 'BIOMD0000000182', 'BIOMD0000000183', 'BIOMD0000000184', 'BIOMD0000000185',
	'BIOMD0000000186', 'BIOMD0000000187', 'BIOMD0000000188', 'BIOMD0000000189', 'BIOMD0000000190',
	'BIOMD0000000191', 'BIOMD0000000192', 'BIOMD0000000193', 'BIOMD0000000194', 'BIOMD0000000195',
	'BIOMD0000000196', 'BIOMD0000000197', 'BIOMD0000000198', 'BIOMD0000000199', 'BIOMD0000000200',
	'BIOMD0000000201', 'BIOMD0000000202', 'BIOMD0000000203', 'BIOMD0000000204', 'BIOMD0000000205',
	'BIOMD0000000206', 'BIOMD0000000207', 'BIOMD0000000208', 'BIOMD0000000209', 'BIOMD0000000210',
	'BIOMD0000000211', 'BIOMD0000000212', 'BIOMD0000000213', 'BIOMD0000000214', 'BIOMD0000000215',
	'BIOMD0000000216', 'BIOMD0000000217', 'BIOMD0000000218', 'BIOMD0000000219', 'BIOMD0000000220',
	'BIOMD0000000221', 'BIOMD0000000222', 'BIOMD0000000223', 'BIOMD0000000224', 'BIOMD0000000225',
	'BIOMD0000000226', 'BIOMD0000000227', 'BIOMD0000000228', 'BIOMD0000000229', 'BIOMD0000000230',
	'BIOMD0000000231', 'BIOMD0000000232', 'BIOMD0000000233', 'BIOMD0000000234', 'BIOMD0000000235',
	'BIOMD0000000236', 'BIOMD0000000237', 'BIOMD0000000238', 'BIOMD0000000239', 'BIOMD0000000240',
	'BIOMD0000000241', 'BIOMD0000000242', 'BIOMD0000000243', 'BIOMD0000000244', 'BIOMD0000000245',
	'BIOMD0000000246', 'BIOMD0000000247', 'BIOMD0000000248', 'BIOMD0000000249', 'BIOMD0000000250',
	'BIOMD0000000251', 'BIOMD0000000252', 'BIOMD0000000253', 'BIOMD0000000254', 'BIOMD0000000255',
	'BIOMD0000000256', 'BIOMD0000000257', 'BIOMD0000000258', 'BIOMD0000000259', 'BIOMD0000000260',
	'BIOMD0000000261', 'BIOMD0000000262', 'BIOMD0000000263', 'BIOMD0000000264', 'BIOMD0000000265',
	'BIOMD0000000266', 'BIOMD0000000267', 'BIOMD0000000268', 'BIOMD0000000269', 'BIOMD0000000270',
	'BIOMD0000000271', 'BIOMD0000000272', 'BIOMD0000000273', 'BIOMD0000000274', 'BIOMD0000000275',
	'BIOMD0000000276', 'BIOMD0000000277', 'BIOMD0000000278', 'BIOMD0000000279', 'BIOMD0000000280',
	'BIOMD0000000281', 'BIOMD0000000282', 'BIOMD0000000283', 'BIOMD0000000284', 'BIOMD0000000285',
	'BIOMD0000000286', 'BIOMD0000000287', 'BIOMD0000000288', 'BIOMD0000000289', 'BIOMD0000000290',
	'BIOMD0000000291', 'BIOMD0000000292', 'BIOMD0000000293', 'BIOMD0000000294', 'BIOMD0000000295',
	'BIOMD0000000296', 'BIOMD0000000297', 'BIOMD0000000298', 'BIOMD0000000299', 'BIOMD0000000300',
	'BIOMD0000000301', 'BIOMD0000000302', 'BIOMD0000000303', 'BIOMD0000000304', 'BIOMD0000000305',
	'BIOMD0000000306', 'BIOMD0000000307', 'BIOMD0000000308', 'BIOMD0000000309', 'BIOMD0000000310',
	'BIOMD0000000311', 'BIOMD0000000312', 'BIOMD0000000313', 'BIOMD0000000314', 'BIOMD0000000315',
	'BIOMD0000000316', 'BIOMD0000000317', 'BIOMD0000000318', 'BIOMD0000000319', 'BIOMD0000000320',
	'BIOMD0000000321', 'BIOMD0000000322', 'BIOMD0000000323', 'BIOMD0000000324', 'BIOMD0000000325',
	'BIOMD0000000326', 'BIOMD0000000327', 'BIOMD0000000328', 'BIOMD0000000329', 'BIOMD0000000330',
	'BIOMD0000000331', 'BIOMD0000000332', 'BIOMD0000000333', 'BIOMD0000000334', 'BIOMD0000000335',
	'BIOMD0000000336', 'BIOMD0000000337', 'BIOMD0000000338', 'BIOMD0000000339', 'BIOMD0000000340',
	'BIOMD0000000341', 'BIOMD0000000342', 'BIOMD0000000343', 'BIOMD0000000344', 'BIOMD0000000345',
	'BIOMD0000000346', 'BIOMD0000000347', 'BIOMD0000000348', 'BIOMD0000000349', 'BIOMD0000000350',
	'BIOMD0000000351', 'BIOMD0000000352', 'BIOMD0000000353', 'BIOMD0000000354', 'BIOMD0000000355',
	'BIOMD0000000356', 'BIOMD0000000357', 'BIOMD0000000358', 'BIOMD0000000359', 'BIOMD0000000360',
	'BIOMD0000000361', 'BIOMD0000000362', 'BIOMD0000000363', 'BIOMD0000000364', 'BIOMD0000000365',
	'BIOMD0000000366', 'BIOMD0000000367', 'BIOMD0000000368', 'BIOMD0000000369', 'BIOMD0000000370',
	'BIOMD0000000371', 'BIOMD0000000372', 'BIOMD0000000373', 'BIOMD0000000374', 'BIOMD0000000375',
	'BIOMD0000000376', 'BIOMD0000000377', 'BIOMD0000000378', 'BIOMD0000000379', 'BIOMD0000000380',
	'BIOMD0000000381', 'BIOMD0000000382', 'BIOMD0000000383', 'BIOMD0000000384', 'BIOMD0000000385',
	'BIOMD0000000386', 'BIOMD0000000387', 'BIOMD0000000388', 'BIOMD0000000389', 'BIOMD0000000390',
	'BIOMD0000000391', 'BIOMD0000000392', 'BIOMD0000000393', 'BIOMD0000000394', 'BIOMD0000000395',
	'BIOMD0000000396', 'BIOMD0000000397', 'BIOMD0000000398', 'BIOMD0000000399', 'BIOMD0000000400',
	'BIOMD0000000401', 'BIOMD0000000402', 'BIOMD0000000403', 'BIOMD0000000404', 'BIOMD0000000405',
	'BIOMD0000000406', 'BIOMD0000000407', 'BIOMD0000000408', 'BIOMD0000000409', 'BIOMD0000000410',
	'BIOMD0000000411', 'BIOMD0000000412', 'BIOMD0000000413', 'BIOMD0000000414', 'BIOMD0000000415',
	'BIOMD0000000416', 'BIOMD0000000417', 'BIOMD0000000418', 'BIOMD0000000419', 'BIOMD0000000420',
	'BIOMD0000000421', 'BIOMD0000000422', 'BIOMD0000000423', 'BIOMD0000000424', 'BIOMD0000000425',
	'BIOMD0000000426', 'BIOMD0000000427', 'BIOMD0000000428', 'BIOMD0000000429', 'BIOMD0000000430',
	'BIOMD0000000431', 'BIOMD0000000432', 'BIOMD0000000433', 'BIOMD0000000434', 'BIOMD0000000435',
	'BIOMD0000000436', 'BIOMD0000000437', 'BIOMD0000000438', 'BIOMD0000000439', 'BIOMD0000000440',
	'BIOMD0000000441', 'BIOMD0000000442', 'BIOMD0000000443', 'BIOMD0000000444', 'BIOMD0000000445',
	'BIOMD0000000446', 'BIOMD0000000447', 'BIOMD0000000448', 'BIOMD0000000449', 'BIOMD0000000450',
	'BIOMD0000000451', 'BIOMD0000000452', 'BIOMD0000000453', 'BIOMD0000000454', 'BIOMD0000000455',
	'BIOMD0000000456', 'BIOMD0000000457', 'BIOMD0000000458', 'BIOMD0000000459', 'BIOMD0000000460',
	'BIOMD0000000461', 'BIOMD0000000462', 'BIOMD0000000463', 'BIOMD0000000464', 'BIOMD0000000465',
	'BIOMD0000000466', 'BIOMD0000000467', 'BIOMD0000000468', 'BIOMD0000000469', 'BIOMD0000000470',
	'BIOMD0000000471', 'BIOMD0000000472', 'BIOMD0000000473', 'BIOMD0000000474', 'BIOMD0000000475',
	'BIOMD0000000476', 'BIOMD0000000477', 'BIOMD0000000478', 'BIOMD0000000479', 'BIOMD0000000480',
	'BIOMD0000000481', 'BIOMD0000000482', 'BIOMD0000000483', 'BIOMD0000000484', 'BIOMD0000000485',
	'BIOMD0000000486', 'BIOMD0000000487', 'BIOMD0000000488', 'BIOMD0000000489', 'BIOMD0000000490',
	'BIOMD0000000491', 'BIOMD0000000492', 'BIOMD0000000493', 'BIOMD0000000494', 'BIOMD0000000495',
	'BIOMD0000000496', 'BIOMD0000000497', 'BIOMD0000000498', 'BIOMD0000000499', 'BIOMD0000000500',
	'BIOMD0000000501', 'BIOMD0000000502', 'BIOMD0000000503', 'BIOMD0000000504', 'BIOMD0000000505',
	'BIOMD0000000506', 'BIOMD0000000507', 'BIOMD0000000508', 'BIOMD0000000509', 'BIOMD0000000510',
	'BIOMD0000000511', 'BIOMD0000000512', 'BIOMD0000000513', 'BIOMD0000000514', 'BIOMD0000000515',
	'BIOMD0000000516', 'BIOMD0000000517', 'BIOMD0000000518', 'BIOMD0000000519', 'BIOMD0000000520',
	'BIOMD0000000521', 'BIOMD0000000522', 'BIOMD0000000523', 'BIOMD0000000524', 'BIOMD0000000525',
	'BIOMD0000000526', 'BIOMD0000000527', 'BIOMD0000000528', 'BIOMD0000000529', 'BIOMD0000000530',
	'BIOMD0000000531', 'BIOMD0000000532', 'BIOMD0000000533', 'BIOMD0000000534', 'BIOMD0000000535',
	'BIOMD0000000536', 'BIOMD0000000537', 'BIOMD0000000538', 'BIOMD0000000539', 'BIOMD0000000540',
	'BIOMD0000000541', 'BIOMD0000000542', 'BIOMD0000000543', 'BIOMD0000000544', 'BIOMD0000000545',
	'BIOMD0000000546', 'BIOMD0000000547', 'BIOMD0000000548', 'BIOMD0000000549', 'BIOMD0000000550',
	'BIOMD0000000551', 'BIOMD0000000552', 'BIOMD0000000553', 'BIOMD0000000554', 'BIOMD0000000555',
	'BIOMD0000000556', 'BIOMD0000000557', 'BIOMD0000000558', 'BIOMD0000000559', 'BIOMD0000000560',
	'BIOMD0000000561', 'BIOMD0000000562', 'BIOMD0000000563', 'BIOMD0000000564', 'BIOMD0000000565',
	'BIOMD0000000566', 'BIOMD0000000567', 'BIOMD0000000568', 'BIOMD0000000569', 'BIOMD0000000570',
	'BIOMD0000000571', 'BIOMD0000000572', 'BIOMD0000000573', 'BIOMD0000000574', 'BIOMD0000000575',
	'BIOMD0000000576', 'BIOMD0000000577', 'BIOMD0000000578', 'BIOMD0000000579', 'BIOMD0000000580',
	'BIOMD0000000581', 'BIOMD0000000582', 'BIOMD0000000583', 'BIOMD0000000584', 'BIOMD0000000585',
	'BIOMD0000000586', 'BIOMD0000000587', 'BIOMD0000000588', 'BIOMD0000000589', 'BIOMD0000000590',
	'BIOMD0000000591', 'BIOMD0000000592', 'BIOMD0000000593', 'BIOMD0000000594', 'BIOMD0000000595',
	'BIOMD0000000596', 'BIOMD0000000597', 'BIOMD0000000598', 'BIOMD0000000599', 'BIOMD0000000600',
	'BIOMD0000000601', 'BIOMD0000000602', 'BIOMD0000000603', 'BIOMD0000000604', 'BIOMD0000000605',
	'BIOMD0000000606', 'BIOMD0000000607', 'BIOMD0000000608', 'BIOMD0000000609', 'BIOMD0000000610',
	'BIOMD0000000611', 'BIOMD0000000612'];

var colors = ["#FFB300",   "#803E75",   "#FF6800",   "#A6BDD7",   "#C10020",   "#CEA262",   "#817066",   "#007D34",
    "#F6768E",   "#00538A",   "#FF7A5C",   "#53377A",   "#FF8E00",   "#B32851",   "#F4C800",  "#7F180D",   "#93AA00",
    "#593315",   "#F13A13",   "#232C16"];

var start_list_ids = 0;
var len_list_ids = 10;
var signetsim_trajectories = {};
var copasi_trajectories = {};
var differences_trajectories = {};
var done_reading = [];

var config_signetsim =
{
    type: 'line',

    data:
    {
        datasets: [],
    },

    title:
    {
      display: true,
      text: "Signetsim simulation results",

    },


    legend:
    {
        display: true,
        position: 'bottom',
        fullWidth: true,
    },

    options:
    {
        scales:
        {
            xAxes: [{
                type: 'linear',
                scaleLabel:
                {
                    display: true,
                    fontStyle: "bold",
                    labelString: 'Time'
                },
                position: 'bottom',
                ticks: {
                    beginAtZero: true,
                }
            }],
            yAxes: [
            {
                display: true,
                scaleLabel:
                {
                    display: true,
                    fontStyle: "bold",
                    labelString: 'Concentration'
                },
                ticks: {
                    beginAtZero: true,
                }
            }],
        }
    }
};

var config_copasi =
{
    type: 'line',

    data:
    {
        datasets: [],
    },

    title:
    {
      display: true,
      text: "Copasi simulation results",

    },


    legend:
    {
        display: true,
        position: 'bottom',
        fullWidth: true,
    },

    options:
    {
        scales:
        {
            xAxes: [
            {
                type: 'linear',
                scaleLabel:
                {
                    display: true,
                    fontStyle: "bold",
                    labelString: 'Time'
                },
                position: 'bottom',
                ticks: {
                    beginAtZero: true,
                }
            }
            ],
            yAxes: [
            {
                display: true,
                scaleLabel:
                {
                    display: true,
                    fontStyle: "bold",
                    labelString: 'Concentration'
                },
                ticks: {
                    beginAtZero: true,
                }
            }],
        }
    }
};

var config_differences =
{
    type: 'line',

    data:
    {
        datasets: [],
    },

    title:
    {
      display: true,
      text: "Differences in simulation results",
    },


    legend:
    {
        display: true,
        position: 'bottom',
        fullWidth: true,
    },

    options:
    {
        scales:
        {
            xAxes: [
            {
                type: 'linear',
                scaleLabel:
                {
                    display: true,
                    fontStyle: "bold",
                    labelString: 'Time'
                },
                position: 'bottom',
                ticks: {
                    beginAtZero: true,
                }
            }
            ],
            yAxes: [
            {
                display: true,
                scaleLabel:
                {
                    display: true,
                    fontStyle: "bold",
                    labelString: 'Differences'
                },
                ticks: {
                    beginAtZero: true,
                }
            }],
        }
    }
};

function compute_differences()
{
    var i=0;
    differences_trajectories = {};

    $.each(signetsim_trajectories, function(key, values)
    {
        if (i == 0)
        {
            differences_trajectories[key] = [];
            $.each(values, function(index, value)
            {
                if (copasi_trajectories[key].indexOf(signetsim_trajectories[key][index]) != -1)
                {
                    differences_trajectories[key][index] = signetsim_trajectories[key][index];
                }
            });
            // differences_trajectories[key] = values;
        }
        else
        {
            if ($.inArray(key, Object.keys(copasi_trajectories)) != -1)
            {
                differences_trajectories[key] = [];
                $.each(values, function(index, value)
                {
                    t_copasi = copasi_trajectories['time'].indexOf(signetsim_trajectories['time'][index]);
                    differences_trajectories[key][index] = Math.abs(value-copasi_trajectories[key][t_copasi]);
                });
            }
        }

        i = i+1;

    });
}

function draw_graph_signetsim ()
{
    var i = 0;
    var times;
    config_signetsim.data.datasets = [];

    $.each(signetsim_trajectories, function(key, values)
    {
        if (i == 0)
            times = values;

        else
        {
            config_signetsim.data.datasets[i-1] = {label: key, data: [], fill: false, backgroundColor: colors[i-1]};

            $.each(values, function(index, value) {
               config_signetsim.data.datasets[i-1].data.push({x: times[index], y: value});
            });
        }

        i = i+1;

    });

    make_graph_signetsim();
}


function draw_graph_copasi ()
{
    var i = 0;
    var times;
    config_copasi.data.datasets = [];

    $.each(copasi_trajectories, function(key, values)
    {
        if (i == 0)
            times = values;

        else
        {
            config_copasi.data.datasets[i-1] = {label: key, data: [], fill: false, backgroundColor: colors[i-1]};

            $.each(values, function(index, value) {
               config_copasi.data.datasets[i-1].data.push({x: times[index], y: value});
            });
        }

        i = i+1;

    });

    make_graph_copasi();
}


function draw_graph_differences ()
{
    var i = 0;
    var times;
    config_differences.data.datasets = [];

    $.each(differences_trajectories, function(key, values)
    {
        if (i == 0)
            times = values;

        else
        {
            config_differences.data.datasets[i-1] = {label: key, data: [], fill: false, backgroundColor: colors[i-1]};

            $.each(values, function(index, value) {
               config_differences.data.datasets[i-1].data.push({x: times[index], y: value});
            });
        }

        i = i+1;

    });

    make_graph_differences();
}
function parseResult(raw_text)
{
    var temp_data = {};
    var lines = raw_text.split('\n');
    var list_species = lines[0].slice(3,-1).split(',');

    $.each(list_species, function (index, value) {
       temp_data[value.trim().slice(1, -1)] = [];
    });

    $.each(lines, function (index, value)
    {

        if (index > 0 && value.trim() != "")
        {
            values = value.split(' ');
            $.each(values, function(sub_index, sub_value)
            {
                temp_data[list_species[sub_index].trim().slice(1, -1)][index-1] = parseFloat(sub_value);
            });
        }
    });
    return temp_data;

}

function readSigNetSimResult(case_id, deferred_signetsim)
{
    var textfile;
    var filename = "cases/" + case_id + "/results_simulated.csv";
    var deferred_signetsim = new $.Deferred();

    if (window.XMLHttpRequest)
    {
        textfile = new XMLHttpRequest();
    }

    textfile.onreadystatechange = function ()
    {
        if (textfile.readyState == 4 && textfile.status == 200)
        {
            signetsim_trajectories = parseResult(textfile.responseText);
            deferred_signetsim.resolve();
        }
    };

    textfile.open("GET", filename , true);
    textfile.overrideMimeType('text/plain');
    textfile.send();

    done_reading.push(deferred_signetsim);
}

function readCopasiResult(case_id)
{
    var textfile;
    var filename = "cases/" + case_id + "/results.csv";
    var deferred_copasi = new $.Deferred();

    if (window.XMLHttpRequest)
    {
        textfile = new XMLHttpRequest();
    }

    textfile.onreadystatechange = function ()
    {
        if (textfile.readyState == 4 && textfile.status == 200)
        {
            copasi_trajectories = parseResult(textfile.responseText);
            deferred_copasi.resolve();
        }
    };

    textfile.open("GET", filename , true);
    textfile.overrideMimeType('text/plain');
    textfile.send();

    done_reading.push(deferred_copasi);
}

function draw_case(case_id)
{
    $("#model_id").empty();
    $("#model_id").append(case_id);
    readSigNetSimResult(case_id);
	readCopasiResult(case_id);

	$.when.apply($, done_reading).then(function() {
        compute_differences();
        draw_graph_signetsim();
        draw_graph_copasi();
        draw_graph_differences();
    });
}

function draw_list()
{
	$('#list_models').empty();
	$.each(list_ids, function( index, value )
	{
		if (index >= start_list_ids && index < (start_list_ids+len_list_ids))
			$('#list_models').append("&nbsp;&nbsp;<a onclick=\"draw_case('" + value.toString() + "');\">" + value.toString() + "</a>&nbsp;&nbsp;");
	});
}

function list_previous()
{
	start_list_ids = Math.max(0, start_list_ids-10);
	draw_list();
}

function list_next()
{
	start_list_ids = Math.min(613, start_list_ids+10);
	draw_list();
}

function make_graph_signetsim ()
{
    var canvas_signetsim = document.getElementById("canvas_signetsim").getContext("2d");
    canvas_signetsim.canvas.height = canvas_signetsim.canvas.width*0.4;
    new Chart(canvas_signetsim, config_signetsim);

}

function make_graph_copasi ()
{
    var canvas_copasi = document.getElementById("canvas_copasi").getContext("2d");
    canvas_copasi.canvas.height = canvas_copasi.canvas.width*0.4;
    new Chart(canvas_copasi, config_copasi);

}

function make_graph_differences ()
{
    var canvas_differences = document.getElementById("canvas_differences").getContext("2d");
    canvas_differences.canvas.height = canvas_differences.canvas.width*0.2;
    new Chart(canvas_differences, config_differences);

}

$( document ).ready(function()
{
	draw_list();

	make_graph_signetsim();
	make_graph_copasi();
    make_graph_differences();
});
