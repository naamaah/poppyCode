#include <nuitrack/Nuitrack.h>

#include <signal.h>
#include <iomanip>
#include <iostream>
#include <fstream>

#include<stdio.h>;
#include<winsock2.h>;
#include<Ws2tcpip.h>;

#pragma comment(lib,"ws2_32.lib") //Winsock Library
#pragma warning(disable:4996) 

#define SERVER "127.0.0.1"	//ip address of udp server
#define BUFLEN 512	//Max length of buffer
#define PORT 8888	//The port on which to listen for incoming data

using namespace tdv::nuitrack;

void showHelpInfo()
{
	std::cout << "Usage: nuitrack_console_sample [path/to/nuitrack.config]" << std::endl;
}

const char* enumToString(JointType jointT) {
	const char* type;
	if (jointT == 1)
		type = "1";
	else
		if (jointT == 2)
			type = "2";
		else
			if (jointT == 3)
				type = "3";
			else
				if (jointT == 4)
					type = "4";
				else
					if (jointT == 5)
						type = "5";
					else
						if (jointT == 6)
							type = "6";
						else
							if (jointT == 7)
								type = "7";
							else
								if (jointT == 8)
									type = "8";
								else
									if (jointT == 9)
										type = "9";
									else
										if (jointT == 11)
											type = "11";
										else
											if (jointT == 12)
												type = "12";
											else
												if (jointT == 13)
													type = "13";
												else
													if (jointT == 14)
														type = "14";
													else
														if (jointT == 15)
															type = "15";
														else
															if (jointT == 17)
																type = "17";
															else
																if (jointT == 18)
																	type = "18";
																else
																	if (jointT == 19)
																		type = "19";
																	else
																		if (jointT == 20)
																			type = "20";
																		else
																			if (jointT == 21)
																				type = "21";
																			else
																				if (jointT == 22)
																					type = "22";
																				else
																					type = "23";
	return type;
}

// Callback for the hand data update event
void onSkeletonUpdate(SkeletonData::Ptr skeletonData)
{
	// -------------For Client-------------------
	struct sockaddr_in si_other;
	int s, slen = sizeof(si_other);
	char buf[BUFLEN];
	char message[BUFLEN];
	WSADATA wsa;
	if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
	{
		printf("Failed. Error Code : %d", WSAGetLastError());
		exit(EXIT_FAILURE);
	}

	//create socket
	if ((s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == SOCKET_ERROR)
	{
		printf("socket() failed with error code : %d", WSAGetLastError());
		exit(EXIT_FAILURE);
	}

	//setup address structure
	memset((char*)&si_other, 0, sizeof(si_other));
	si_other.sin_family = AF_INET;
	si_other.sin_port = htons(PORT);
	si_other.sin_addr.S_un.S_addr = inet_addr(SERVER);

	if (!skeletonData)
	{
		// No skeleton data
		std::cout << "No Skeleton data" << std::endl;
		return;
	}

	auto userSkeleton = skeletonData->getSkeletons();
	if (userSkeleton.empty())
	{
		// No skeleton hands
		return;
	}

	auto joints = userSkeleton[0].joints; //user one joints
	std::vector <Joint> jointsVector; //just the joints i need
	jointsVector.push_back(joints[1]); //JOINT_HEAD
	jointsVector.push_back(joints[2]); //JOINT_NECK
	jointsVector.push_back(joints[3]); //JOINT_TORSO
	jointsVector.push_back(joints[4]); //JOINT_WAIST
	jointsVector.push_back(joints[5]); //JOINT_LEFT_COLLAR
	jointsVector.push_back(joints[6]); //JOINT_LEFT_SHOULDER
	jointsVector.push_back(joints[7]); //JOINT_LEFT_ELBOW
	jointsVector.push_back(joints[8]);//JOINT_LEFT_WRIST
	jointsVector.push_back(joints[9]); //JOINT_LEFT_HAND
	jointsVector.push_back(joints[11]); //JOINT_RIGHT_COLLAR
	jointsVector.push_back(joints[12]); //JOINT_RIGHT_SHOULDER
	jointsVector.push_back(joints[13]); //JOINT_RIGHT_ELBOW
	jointsVector.push_back(joints[14]);//JOINT_RIGHT_WRIST
	jointsVector.push_back(joints[15]); //JOINT_RIGHT_HAND
	jointsVector.push_back(joints[17]); //JOINT_LEFT_HIP
	jointsVector.push_back(joints[18]); //JOINT_LEFT_KNEE
	jointsVector.push_back(joints[19]); //JOINT_LEFT_ANKLE
	jointsVector.push_back(joints[21]); //JOINT_RIGHT_HIP
	jointsVector.push_back(joints[22]); //JOINT_RIGHT_KNEE
	jointsVector.push_back(joints[23]); //JOINT_RIGHT_ANKLE

	strncpy(message, "", sizeof(message));
	std::cout << std::fixed << std::setprecision(3);
	for (const auto j : jointsVector) {
		if (j.confidence > 0.5) {
			time_t my_time = time(NULL);
			std::cout << j.type << ","
				<< j.real.x << ", "
				<< j.real.y << ", "
				<< j.real.z << std::endl;
			//myfile << j.type << "," //write in file
			//	<<j.real.x << ","
			//	<<j.real.y << ","
			//	<<j.proj.z << std::endl;

		//send client message: change float values to char and combine to message
			strncat(message, enumToString(j.type), sizeof(message));
			strncat(message, ",", sizeof(message));
			char xf[10];
			float x = j.real.x;
			sprintf(xf, "%1.2f", j.real.x);
			strncat(message, xf, sizeof(message));
			strncat(message, ",", sizeof(message));
			char yf[10];
			float y = j.real.y;
			sprintf(yf, "%1.2f", y);
			strncat(message, yf, sizeof(message));
			strncat(message, ",", sizeof(message));
			char zf[10];
			float z = j.real.z;
			sprintf(zf, "%1.2f", z);
			strncat(message, zf, sizeof(message));
			if (j.type != 3)
				strncat(message, "/", sizeof(message));
		}
	}
	sendto(s, (message), strlen(message), 0, (struct sockaddr*)&si_other, slen);
	//std::chrono::milliseconds dura(500);
	//std::this_thread::sleep_for(dura);
}

bool finished;
void signalHandler(int signal)
{
	if (signal == SIGINT)
		finished = true;
}

int main(int argc, char* argv[])
{
	showHelpInfo();

	signal(SIGINT, &signalHandler);

	std::string configPath = "";
	if (argc > 1)
		configPath = argv[1];

	// Initialize Nuitrack
	try
	{
		Nuitrack::init(configPath);
	}
	catch (const Exception& e)
	{
		std::cerr << "Can not initialize Nuitrack (ExceptionType: " << e.type() << ")" << std::endl;
		return EXIT_FAILURE;
	}

	// Create HandTracker module, other required modules will be
	// created automatically
	auto skeletonTracker = SkeletonTracker::create();

	// Connect onHandUpdate callback to receive hand tracking data
	skeletonTracker->connectOnUpdate(onSkeletonUpdate);

	// Start Nuitrack
	try
	{
		Nuitrack::run();
	}
	catch (const Exception& e)
	{
		std::cerr << "Can not start Nuitrack (ExceptionType: " << e.type() << ")" << std::endl;
		return EXIT_FAILURE;
	}

	int errorCode = EXIT_SUCCESS;
	while (!finished)
	{
		try
		{
			// Wait for new skeleton tracking data
			Nuitrack::waitUpdate(skeletonTracker);
		}
		catch (LicenseNotAcquiredException& e)
		{
			std::cerr << "LicenseNotAcquired exception (ExceptionType: " << e.type() << ")" << std::endl;
			errorCode = EXIT_FAILURE;
			break;
		}
		catch (const Exception& e)
		{
			std::cerr << "Nuitrack update failed (ExceptionType: " << e.type() << ")" << std::endl;
			errorCode = EXIT_FAILURE;
		}
	}

	// Release Nuitrack
	try
	{
		Nuitrack::release();
	}
	catch (const Exception& e)
	{
		std::cerr << "Nuitrack release failed (ExceptionType: " << e.type() << ")" << std::endl;
		errorCode = EXIT_FAILURE;
	}

	return errorCode;
}